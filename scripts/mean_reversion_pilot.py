#!/usr/bin/env python3
"""Guarded daily mean-reversion paper pilot; dry-run default, never scheduled."""
import argparse
import fcntl
import json
import math
import os
import sys
import threading
import uuid
from datetime import datetime, timezone, time as clock
from pathlib import Path
from zoneinfo import ZoneInfo
from shadow_experiments import SYMBOLS, daily_mean_reversion
import yfinance as yf
from datetime import timedelta, date
from manage_positions import ACCOUNT, broker_snapshot, trader
from scan_watchlist import fetch_quotes, quote_quality

STATE = Path.home() / '.openclaw/state/wyckoff-experiments'
LEDGER = STATE / 'mean_reversion.jsonl'
REF = 'EXP-MEAN-REVERSION'
ET = ZoneInfo('America/New_York')
CAPITAL = 80000
GROSS_CAP = 80000
NAME_CAP = 10000
RISK_BUDGET = CAPITAL * .0025


def append(row):
    STATE.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a') as f:
        f.write(json.dumps({'at': datetime.now(timezone.utc).isoformat(), 'ref': REF, **row}) + '\n')
        f.flush()
        os.fsync(f.fileno())


def inventory(rows, positions, today):
    owned, daily = {}, set()
    intents = [r for r in rows if r.get('event') == 'intent']
    keys = [r.get('intent_id', r['id']) for r in intents]
    if len(keys) != len(set(keys)):
        raise RuntimeError('duplicate intent ids; manual broker reconciliation required')
    resolved = {r.get('intent_id', r['id']) for r in rows if r.get('event') == 'resolved'}
    if any(k not in resolved for k in keys):
        raise RuntimeError('unresolved order intent; manual broker reconciliation required')
    for r in rows:
        if r.get('event') == 'fill':
            s = r['symbol']
            owned[s] = owned.get(s, 0) + int(r['qty']) * (1 if r['side'] == 'BUY' else -1)
            if r['side'] == 'BUY' and r.get('day') == today:
                daily.add(s)
    for s, qty in owned.items():
        broker = positions.get((ACCOUNT, s))
        if qty < 0 or (qty and (not broker or broker[0] != qty or broker[2:] != ('STK', 'USD'))) or (not qty and broker):
            raise RuntimeError('ledger/broker holding mismatch: ' + s)
    return {s: q for s, q in owned.items() if q}, daily


def session(now):
    # Known 2026 NYSE closures; unknown calendar years fail closed.
    holidays = {'2026-01-01', '2026-01-19', '2026-02-16', '2026-04-03',
                '2026-05-25', '2026-06-19', '2026-07-03', '2026-09-07',
                '2026-11-26', '2026-12-25'}
    et = now.astimezone(ET)
    return (et.year == 2026 and et.weekday() < 5 and et.date().isoformat() not in holidays
            and clock(9, 35) <= et.time() < clock(15, 55))


def quote(symbol, reference=None):
    quotes, error = fetch_quotes([symbol])
    q = quotes.get(symbol, {})
    spread, quality = quote_quality(q, datetime.now(timezone.utc))
    try:
        stamp = datetime.fromisoformat(str(q['timestamp']).replace('Z', '+00:00'))
        age = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
        bid, ask = float(q['bid']), float(q['ask'])
    except (KeyError, ValueError, TypeError):
        raise RuntimeError('missing quote data: ' + symbol)
    if error or quality != 'OK' or spread is None or not 0 <= age <= 90 or stamp.astimezone(ET).date() != datetime.now(ET).date() or not all(math.isfinite(x) and x > 0 for x in (bid, ask)) or ask < bid or spread > .005 or (reference and abs(ask / reference - 1) > .01):
        raise RuntimeError('stale/wide/unmatched quote: ' + symbol)
    return bid, ask


def execution_snapshot(app, oid, symbol, side, intent_id):
    """Collect the complete broker response; status alone never establishes a fill."""
    from ibapi.execution import ExecutionFilter
    done = threading.Event()
    executions = {}
    req_id = 710000 + (uuid.uuid4().int % 1000000)
    old_detail, old_end, old_error = app.execDetails, app.execDetailsEnd, app.error
    errors = []
    def on_error(request, code, message, *args):
        old_error(request, code, message, *args)
        if code not in (2104, 2106, 2158, 2186):
            errors.append((request, code))
    def detail(request, contract, execution):
        if request == req_id:
            if (execution.acctNumber == ACCOUNT and execution.orderRef == intent_id
                    and execution.orderId == oid and contract.symbol == symbol
                    and contract.secType == 'STK' and contract.currency == 'USD'
                    and execution.side == ('BOT' if side == 'BUY' else 'SLD')):
                executions[execution.execId] = execution.shares
        else:
            old_detail(request, contract, execution)
    def end(request):
        if request == req_id: done.set()
        else: old_end(request)
    app.execDetails, app.execDetailsEnd, app.error = detail, end, on_error
    try:
        filt = ExecutionFilter()
        filt.acctCode = ACCOUNT
        app.reqExecutions(req_id, filt)
        if not done.wait(15) or errors or not app.isConnected():
            raise RuntimeError('execution snapshot incomplete/API error; intent retained')
        if any(int(q) != q or q <= 0 for q in executions.values()):
            raise RuntimeError('invalid execution quantity; intent retained')
        return sum(int(q) for q in executions.values())
    finally:
        app.execDetails, app.execDetailsEnd, app.error = old_detail, old_end, old_error


def submit(app, symbol, side, qty, price, before):
    """Persist intent BEFORE submission; never infer cancellation implies no fills."""
    oid = app.next_order_id
    if not isinstance(oid, int) or oid < 1:
        raise RuntimeError('missing broker order ID')
    contract = trader.Contract()
    contract.symbol, contract.secType, contract.exchange, contract.currency = symbol, 'STK', 'SMART', 'USD'
    order = trader.Order()
    order.action, order.orderType, order.tif = side, 'LMT', 'DAY'
    order.totalQuantity, order.lmtPrice = qty, round(price * (1.001 if side == 'BUY' else .999), 2)
    intent_id = REF + '-' + uuid.uuid4().hex
    order.account, order.orderRef = ACCOUNT, intent_id
    order.eTradeOnly = order.firmQuoteOnly = False
    append({'event': 'intent', 'id': oid, 'intent_id': intent_id, 'symbol': symbol, 'side': side, 'qty': qty})
    print('BROKER_ACTION', side, symbol, qty, 'order_id', oid, 'limit', order.lmtPrice, 'intent', intent_id, flush=True)
    app.placeOrder(oid, contract, order)
    import time
    time.sleep(3)
    result = app.order_results.get(oid)
    if not result or result.get('status') not in ('Filled', 'Cancelled', 'ApiCancelled'):
        app.cancelOrder(oid)
        time.sleep(3)
    status = (app.order_results.get(oid) or {}).get('status')
    app.disconnect()
    check, positions, orders = broker_snapshot(client_id=143)
    try:
        if orders:
            raise RuntimeError('resting order after cancel; intent retained')
        after = positions.get((ACCOUNT, symbol), (0,))[0]
        delta = after - before
        filled = delta if side == 'BUY' else -delta
        if filled < 0 or filled > qty or int(filled) != filled:
            raise RuntimeError('position delta mismatch; intent retained')
        # Shared account: positions alone cannot establish strategy ownership.
        # Snapshot API has no execution/orderRef history; do not attribute a fill without it.
        matched = execution_snapshot(check, oid, symbol, side, intent_id)
        if matched != filled:
            raise RuntimeError('execution/position delta mismatch; intent retained')
        if status not in ('Filled', 'Cancelled', 'ApiCancelled'):
            raise RuntimeError('order status not terminal; intent retained')
        if status == 'Filled' and filled != qty:
            raise RuntimeError('Filled status/quantity mismatch; intent retained')
        if filled:
            append({'event': 'fill', 'id': oid, 'intent_id': intent_id, 'symbol': symbol, 'side': side, 'qty': int(filled), 'day': datetime.now(ET).date().isoformat()})
        append({'event': 'resolved', 'id': oid, 'intent_id': intent_id, 'filled': int(filled)})
        print('BROKER_RESULT', side, symbol, 'verified_filled', int(filled), 'requested', qty, 'broker_status', status, 'open_orders', len(orders))
        return int(filled)
    finally:
        check.disconnect()


HOLIDAYS = {'2026-01-01', '2026-01-19', '2026-02-16', '2026-04-03', '2026-05-25', '2026-06-19', '2026-07-03', '2026-09-07', '2026-11-26', '2026-12-25'}


def trading_days(start, end):
    if start.year != 2026 or end.year != 2026 or start > end:
        raise RuntimeError('unsupported trading calendar/date')
    count = 0
    while start < end:
        start += timedelta(days=1)
        if start.weekday() < 5 and start.isoformat() not in HOLIDAYS: count += 1
    return count


def completed_daily(closes, stamps, now):
    if now.tzinfo is None or len(closes) != len(stamps) or not stamps:
        raise RuntimeError('invalid daily bars')
    today = now.astimezone(ET).date()
    completed = []
    for close, stamp in zip(closes, stamps):
        if stamp.tzinfo is None: raise RuntimeError('naive daily timestamp')
        day = stamp.astimezone(ET).date()
        if day < today: completed.append((day, float(close)))
    if not completed or trading_days(completed[-1][0], today) != 1:
        raise RuntimeError('stale daily signal')
    return [v for _, v in completed], completed[-1][1]


def daily_bars(symbols, now):
    data = yf.download(symbols, period='6mo', interval='1d', auto_adjust=False,
                       progress=False, threads=True, group_by='ticker')
    out = {}
    for symbol in symbols:
        try:
            frame = data[symbol].dropna(subset=['Close'])
            # yfinance daily indices are often naive exchange dates, not UTC instants.
            # Interpret a naive daily label as NY exchange-local midnight.
            stamps = frame.index.tz_localize(ET) if frame.index.tz is None else frame.index
            out[symbol] = completed_daily(list(frame['Close']),
                [stamp.to_pydatetime() for stamp in stamps], now)
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            print('SKIP daily data', symbol, str(exc))
    return out


def entry_allowed(symbol, positions, orders, owned, daily):
    return (symbol not in daily and symbol not in owned and
            not any(s == symbol for _, s in positions) and
            not any(item[0] == symbol for item in orders.values()))


def first_entry(rows, symbol):
    qty, entry = 0, None
    for row in rows:
        if row.get('event') != 'fill' or row.get('symbol') != symbol:
            continue
        fill = int(row['qty'])
        if row['side'] == 'BUY':
            if qty == 0: entry = date.fromisoformat(row['day'])
            qty += fill
        elif row['side'] == 'SELL':
            qty -= fill
            if qty < 0: raise RuntimeError('sell exceeds tagged holding')
            if qty == 0: entry = None
        else:
            raise RuntimeError('unknown tagged fill side')
    if not qty or entry is None: raise RuntimeError('missing active tagged entry for exit')
    return entry


def exit_trigger(bid, basis, entry_day, now):
    return bid <= basis * .96 or bid >= basis * 1.06 or trading_days(entry_day, now.astimezone(ET).date()) >= 5


def run(execute=False, now=None):
    now = now or datetime.now(timezone.utc)
    STATE.mkdir(parents=True, exist_ok=True)
    with (STATE / 'entry.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        app, positions, orders = broker_snapshot(client_id=141)
        try:
            rows = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()] if LEDGER.exists() else []
            today = now.astimezone(ET).date().isoformat()
            owned, daily = inventory(rows, positions, today)
            if orders: raise RuntimeError('broker open orders; no submission')
            if not session(now):
                print('SKIP outside NYSE session; ALERT overnight residuals:', owned)
                return 0
            for symbol, qty in owned.items():
                bid, _ = quote(symbol)
                basis = positions[(ACCOUNT, symbol)][1]
                if exit_trigger(bid, basis, first_entry(rows, symbol), now):
                    print('EXIT', symbol, qty, 'bid', bid)
                    if execute:
                        app.disconnect()
                        app, latest, pending = broker_snapshot(client_id=142)
                        if pending or latest != positions or not session(datetime.now(timezone.utc)):
                            raise RuntimeError('changed broker/session before exit')
                        bid, _ = quote(symbol)
                        if not exit_trigger(bid, basis, first_entry(rows, symbol), datetime.now(timezone.utc)):
                            raise RuntimeError('exit trigger changed')
                        filled = submit(app, symbol, 'SELL', qty, bid, qty)
                        if filled < qty: print('ALERT overnight residual shares require retry')
                        return 0
            if now.astimezone(ET).time() >= clock(14, 30) or sum(r.get('event') == 'fill' and r.get('side') == 'BUY' and r.get('day') == today and int(r.get('qty', 0)) > 0 for r in rows) >= 2:
                print('No new entries; cutoff or daily fill cap'); return 0
            bars = daily_bars(SYMBOLS, now)
            gross = sum(q * positions[(ACCOUNT, s)][1] for s, q in owned.items())
            for symbol in SYMBOLS:
                if not entry_allowed(symbol, positions, orders, owned, daily): continue
                item = bars.get(symbol)
                if not item or not daily_mean_reversion(item[0]): continue
                reference = item[1]
                _, ask = quote(symbol, reference)
                qty = min(math.floor(200 / (ask * .04)), math.floor(10000 / (ask * 1.001)), math.floor((80000 - gross) / (ask * 1.001)))
                if qty < 1: continue
                print('ENTRY', symbol, qty, 'ask', ask, 'planned stop', round(ask * .96, 2))
                if execute:
                    app.disconnect()
                    app, latest, pending = broker_snapshot(client_id=142)
                    if pending or latest != positions or not session(datetime.now(timezone.utc)) or datetime.now(ET).time() >= clock(14, 30):
                        raise RuntimeError('changed broker/session before entry')
                    if not entry_allowed(symbol, latest, pending, owned, daily):
                        raise RuntimeError('duplicate symbol before entry')
                    _, ask = quote(symbol, reference)
                    qty = min(qty, math.floor(200 / (ask * .04)), math.floor(10000 / (ask * 1.001)), math.floor((80000 - gross) / (ask * 1.001)))
                    if qty: submit(app, symbol, 'BUY', qty, ask, 0)
                return 0
            print('No eligible mean-reversion entry')
            return 0
        finally:
            app.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        raise SystemExit(run(args.execute))
    except Exception as exc:
        print('BLOCK', type(exc).__name__, exc)
        raise SystemExit(2)
