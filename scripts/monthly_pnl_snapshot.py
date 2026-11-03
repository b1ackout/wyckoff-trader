#!/usr/bin/env python3
"""Read-only IBKR paper-account P&L snapshots and monthly summaries."""
import argparse
import fcntl
import json
import logging
import math
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import trade_cycle as trader

ACCOUNT = 'DUO957759'
STATE = Path.home() / '.openclaw/state/wyckoff-pnl'
LEDGER = STATE / 'snapshots.jsonl'
ET = ZoneInfo('America/New_York')
CLIENT_ID = 159
IGNORE_ERRORS = {2104, 2106, 2158, 2186}


def fetch_snapshot():
    previous_log_level = logging.getLogger().level
    logging.getLogger().setLevel(logging.WARNING)
    app = trader.IBKRApp()
    accounts, values, errors = [], {}, []
    accounts_done, download_done = threading.Event(), threading.Event()
    app.managedAccounts = lambda ids: (accounts.extend(ids.split(',')), accounts_done.set())
    def on_value(key, value, currency, account):
        if account == ACCOUNT and key in ('NetLiquidation', 'TotalCashValue', '$LEDGER-UnrealizedPnL', '$LEDGER-RealizedPnL'):
            values[(key, currency)] = (value, currency)
    app.updateAccountValue = on_value
    app.accountDownloadEnd = lambda account: download_done.set() if account == ACCOUNT else None
    original_error = app.error
    def on_error(req_id, code, message, *args):
        original_error(req_id, code, message, *args)
        if code not in IGNORE_ERRORS:
            errors.append((code, str(message)[:200]))
    app.error = on_error
    app.connect('127.0.0.1', 7497, clientId=CLIENT_ID)
    threading.Thread(target=app.run, daemon=True).start()
    try:
        deadline = time.monotonic() + 10
        while not app.connected and time.monotonic() < deadline:
            time.sleep(.05)
        if not app.connected or not accounts_done.wait(5) or accounts != [ACCOUNT]:
            raise RuntimeError('paper account connection/identity unavailable')
        app.reqAccountUpdates(True, ACCOUNT)
        if not download_done.wait(10):
            raise RuntimeError('IBKR account update snapshot timed out')
        if errors:
            raise RuntimeError(f'IBKR API error {errors[-1]}')
        nlv_pair = next((v for (k, c), v in values.items() if k == 'NetLiquidation' and c not in ('', 'BASE')), None)
        if nlv_pair is None:
            raise RuntimeError('IBKR NetLiquidation unavailable')
        nlv, currency = float(nlv_pair[0]), nlv_pair[1]
        if not math.isfinite(nlv): raise RuntimeError('IBKR returned invalid NetLiquidation')
        cash_pair = values.get(('TotalCashValue', currency))
        unreal_pair = values.get(('$LEDGER-UnrealizedPnL', 'BASE'))
        realized_pair = values.get(('$LEDGER-RealizedPnL', 'BASE'))
        if cash_pair is None or unreal_pair is None or realized_pair is None:
            raise RuntimeError('IBKR base-currency cash/realized/unrealized fields missing')
        cash, cash_ccy = float(cash_pair[0]), cash_pair[1]
        unrealized, realized = float(unreal_pair[0]), float(realized_pair[0])
        if cash_ccy != currency or not all(math.isfinite(v) and abs(v) < 1e100 for v in (nlv, cash, unrealized, realized)):
            raise RuntimeError('IBKR account values invalid or currencies inconsistent')
        now = datetime.now(timezone.utc)
        return {'event': 'snapshot', 'account': ACCOUNT, 'timestamp_utc': now.isoformat(),
                'date_et': now.astimezone(ET).date().isoformat(), 'currency': currency,
                'net_liquidation': nlv, 'total_cash': cash,
                'realized_daily_pnl_base': realized, 'unrealized_pnl_base': unrealized}
    finally:
        try: app.reqAccountUpdates(False, ACCOUNT)
        except Exception: pass
        app.disconnect()
        logging.getLogger().setLevel(previous_log_level)


def append_row(row):
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(STATE, 0o700)
    with (STATE / 'ledger.lock').open('a') as lock:
        os.chmod(STATE / 'ledger.lock', 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        with LEDGER.open('a') as f:
            os.chmod(LEDGER, 0o600)
            f.write(json.dumps(row, sort_keys=True) + '\n')
            f.flush(); os.fsync(f.fileno())


def load_rows():
    if not LEDGER.exists(): return []
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def latest_per_date(rows, month):
    daily = {}
    for row in rows:
        if row.get('account') != ACCOUNT or row.get('event') not in ('snapshot', 'baseline') or 'unrealized_pnl_base' not in row or 'realized_daily_pnl_base' not in row: continue
        date = row['date_et']
        if date[:7] == month:
            daily[date] = row
    return [daily[d] for d in sorted(daily)]


def summarize_month(rows, month):
    current = latest_per_date(rows, month)
    if not current: return None
    prior = [r for r in rows if r.get('account') == ACCOUNT and r.get('event') == 'snapshot' and r.get('date_et','')[:7] < month and 'unrealized_pnl_base' in r and 'realized_daily_pnl_base' in r]
    prior.sort(key=lambda r: r['timestamp_utc'])
    baseline = prior[-1] if prior else None
    baseline_source = 'previous recorded snapshot' if baseline else 'first snapshot in month (partial history)'
    if baseline is None:
        baselines = [r for r in rows if r.get('account') == ACCOUNT and r.get('event') == 'baseline' and r.get('date_et','')[:7] == month and 'unrealized_pnl_base' in r and 'realized_daily_pnl_base' in r]
        if baselines:
            baselines.sort(key=lambda r: r['timestamp_utc']); baseline = baselines[-1]
            baseline_source = 'explicit starting baseline'
        else:
            baseline = current[0]
    realized = 0.0
    for r in current:
        amount = float(r['realized_daily_pnl_base'])
        if r['date_et'] == baseline['date_et']:
            amount -= float(baseline.get('realized_daily_pnl_base', amount))
        realized += amount
    end = current[-1]
    unrealized_change = float(end['unrealized_pnl_base']) - float(baseline['unrealized_pnl_base'])
    nlv_change = float(end['net_liquidation']) - float(baseline['net_liquidation'])
    pnl_estimate = realized + unrealized_change
    discrepancy = pnl_estimate - nlv_change
    reconciliation = 'MATCH' if abs(discrepancy) <= max(100.0, abs(nlv_change) * .005) else 'REVIEW'
    return {'month': month, 'as_of': end['timestamp_utc'], 'currency': end['currency'],
            'realized_pnl_observed': realized, 'unrealized_change': unrealized_change,
            'total_pnl_estimate': pnl_estimate,
            'net_liquidation_change_before_external_flows': nlv_change,
            'pnl_vs_nlv_discrepancy': discrepancy, 'reconciliation_status': reconciliation,
            'baseline_date_et': baseline['date_et'], 'baseline_source': baseline_source,
            'snapshot_dates': [r['date_et'] for r in current],
            'observed_snapshot_days': len(current),
            'coverage_caveat': 'Realized P&L is summed from recorded daily callbacks; missed days are not backfilled. NLV change is unadjusted for external cash flows.'}


def report_month(rows, month):
    s = summarize_month(rows, month)
    if not s: return f'No paper-account snapshots recorded for {month}.'
    return (f"MONTH {s['month']} as of {s['as_of']} | {s['currency']} | "
            f"realized observed {s['realized_pnl_observed']:+.2f} | "
            f"change in unrealized {s['unrealized_change']:+.2f} | "
            f"P&L estimate {s['total_pnl_estimate']:+.2f} | "
            f"NLV change (before external flows) {s['net_liquidation_change_before_external_flows']:+.2f} | "
            f"P&L/NLV gap {s['pnl_vs_nlv_discrepancy']:+.2f} ({s['reconciliation_status']}) | "
            f"baseline {s['baseline_date_et']} ({s['baseline_source']}) | "
            f"{s['observed_snapshot_days']} snapshot dates; {s['coverage_caveat']}")


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--baseline', action='store_true', help='record a new starting point')
    mode.add_argument('--report', metavar='YYYY-MM', help='print monthly summary without querying TWS')
    args = parser.parse_args(argv)
    if args.report:
        print(report_month(load_rows(), args.report)); return 0
    row = fetch_snapshot()
    if args.baseline:
        row['event'] = 'baseline'
        append_row(row)
        print('PAPER P&L STARTING BASELINE RECORDED', row['timestamp_utc'], row['account'], row['currency'])
        print('Net liquidation', f"{row['net_liquidation']:.2f}", 'realized today (base)', f"{row['realized_daily_pnl_base']:+.2f}", 'open unrealized (base)', f"{row['unrealized_pnl_base']:+.2f}")
        print('Monthly history begins at this timestamp; earlier months need IBKR statement backfill.')
        return 0
    append_row(row)
    print('PAPER P&L SNAPSHOT', row['timestamp_utc'], row['account'], row['currency'])
    print('Net liquidation', f"{row['net_liquidation']:.2f}", 'cash', f"{row['total_cash']:.2f}")
    print('Realized today (base)', f"{row['realized_daily_pnl_base']:+.2f}", 'open unrealized (base)', f"{row['unrealized_pnl_base']:+.2f}")
    month = row['date_et'][:7]
    print(report_month(load_rows(), month))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
