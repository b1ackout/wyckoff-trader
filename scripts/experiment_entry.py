#!/usr/bin/env python3
"""One guarded, tagged Wyckoff paper entry; dry-run unless --execute."""
import argparse
import fcntl
import json
import math
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import trade_cycle as trader
from manage_positions import ACCOUNT, broker_snapshot, market_open
from risk_sizing import proposed_shares
from scan_watchlist import download_batch, fetch_quotes, quote_quality

CAPITAL = 80000.0  # isolated simulated USD strategy sleeve, not whole IBKR account
GROSS_CAP = 20000.0
NAME_CAP = 2500.0
STOP_FRACTION = 0.08
COST_BUFFER = 0.005
ORDER_REF = "EXP-WYCKOFF-RISK025"
STATE = Path.home() / ".openclaw/state/wyckoff-experiments"


def sleeve_exposure(positions):
    """Count only recorded pilot holdings; fail closed on missing/mismatched ledger."""
    ledger = STATE / "trades.jsonl"
    if not ledger.exists():
        raise RuntimeError("experiment fill ledger unavailable")
    recorded = {}
    for line in ledger.read_text().splitlines():
        item = json.loads(line)
        if item.get("strategy") == "WYCKOFF-RISK025" and item.get("status") == "Filled":
            recorded[item["symbol"]] = recorded.get(item["symbol"], 0) + int(item["quantity"])
    gross = 0.0
    for symbol, baseline in recorded.items():
        current = positions.get((ACCOUNT, symbol))
        if current:
            qty, cost, sec, currency = current
            if sec != "STK" or currency != "USD" or qty < 0 or qty > baseline or cost <= 0:
                raise RuntimeError("experiment/broker holding mismatch; manual reconciliation needed")
            gross += qty * cost
    return gross


def today_entries():
    ledger = STATE / "trades.jsonl"
    if not ledger.exists(): raise RuntimeError("experiment fill ledger unavailable")
    today = datetime.now(timezone.utc).date().isoformat()
    return [item["symbol"] for line in ledger.read_text().splitlines()
            if (item := json.loads(line)).get("strategy") == "WYCKOFF-RISK025"
            and item.get("status") == "Filled" and item.get("timestampUtc", "").startswith(today)]


def candidate(symbol):
    quotes, error = fetch_quotes([symbol])
    quote = quotes.get(symbol, {})
    spread, quality = quote_quality(quote, datetime.now(timezone.utc))
    if error or quality != "OK" or spread is None:
        raise RuntimeError(f"unusable {symbol} quote: {error or quality}")
    bars = {tf: download_batch([symbol], period, interval)[symbol] for tf, period, interval in
            (("daily", "3mo", "1d"), ("weekly", "1y", "1wk"), ("monthly", "5y", "1mo"))}
    if any(len(bars[tf]) < 20 for tf in bars):
        raise RuntimeError("insufficient bars")
    signal, reason, frames = trader.analyze_wyckoff_multitf(symbol, quote, bars)
    close = bars["daily"][-1]["c"]
    ask = float(quote["ask"])
    if signal != "LONG" or not math.isfinite(close) or abs(ask / close - 1) > .02:
        raise RuntimeError(f"no executable LONG: {signal}; quote/close disagreement")
    # Model 8% invalidation plus 0.5% cost/slippage reserve; not a guaranteed stop.
    stop = ask * (1 - STOP_FRACTION - COST_BUFFER)
    size = proposed_shares(CAPITAL, ask, stop, 0, GROSS_CAP)
    qty = min(size["proposed_shares"], math.floor(NAME_CAP / ask))
    if qty < 1:
        raise RuntimeError("risk/notional limits leave zero shares")
    return qty, quote, close, stop, frames, size


def auto_symbol():
    """Rank unheld LONG candidates; no quote-quality bypass or forced trade."""
    app, positions, orders = broker_snapshot(client_id=89)
    try:
        if orders:
            raise RuntimeError("broker has outstanding orders")
        if sleeve_exposure(positions) >= GROSS_CAP:
            return None
        entered = today_entries()
        if len(entered) >= 2: return None
        names = [s for s in trader.WATCHLIST if s not in entered and not any(k[1] == s for k in positions)]
    finally:
        app.disconnect()
    if not names:
        return None
    bars = {tf: download_batch(names, period, interval) for tf, period, interval in
            (("daily", "3mo", "1d"), ("weekly", "1y", "1wk"), ("monthly", "5y", "1mo"))}
    quotes, error = fetch_quotes(names)
    if error: raise RuntimeError("candidate quote fetch failed")
    ranked = []
    for symbol in names:
        quote = quotes.get(symbol, {})
        _, quality = quote_quality(quote, datetime.now(timezone.utc))
        series = {tf: bars[tf].get(symbol, []) for tf in bars}
        if quality != "OK" or any(len(series[tf]) < 20 for tf in series): continue
        signal, _, frames = trader.analyze_wyckoff_multitf(symbol, quote, series)
        close = series["daily"][-1]["c"]
        if signal == "LONG" and close > 0 and abs(float(quote["ask"]) / close - 1) <= .02:
            ranked.append((-sum(v == "LONG" for v in frames.values()), trader.WATCHLIST.index(symbol), symbol))
    return min(ranked)[2] if ranked else None


def run(symbol, execute=False):
    if symbol not in trader.WATCHLIST:
        raise RuntimeError("symbol outside canonical watchlist")
    if not market_open(datetime.now(timezone.utc)):
        print("SKIP outside regular-session entry window"); return 0
    app, positions, orders = broker_snapshot(client_id=86)
    try:
        if len(today_entries()) >= 2 or symbol in today_entries():
            print("SKIP daily pilot entry limit"); return 0
        if orders or any(s == symbol for (_, s) in positions):
            print("SKIP existing position or open order; no duplicate entry"); return 0
        gross = sleeve_exposure(positions)
        qty, quote, close, stop, frames, size = candidate(symbol)
        qty = min(qty, math.floor(max(0, GROSS_CAP - gross) / float(quote["ask"])))
        if qty < 1:
            print("SKIP virtual sleeve gross cap reached"); return 0
        print("CANDIDATE", symbol, "LONG", qty, "ask", quote["ask"], "planned_stop", round(stop,2),
              "max_planned_risk_usd", size["risk_budget_usd"], "gross_cap_usd", GROSS_CAP,
              "timeframes", frames)
        if not execute:
            print("DRY RUN: no broker order"); return 0
        app.disconnect()
        app, positions, orders = broker_snapshot(client_id=87)
        if orders or any(s == symbol for (_, s) in positions) or not market_open(datetime.now(timezone.utc)):
            print("BLOCK changed broker state or closed session"); return 2
        gross = sleeve_exposure(positions)
        quotes, error = fetch_quotes([symbol])
        fresh = quotes.get(symbol, {})
        spread, quality = quote_quality(fresh, datetime.now(timezone.utc))
        ask = float(fresh.get("ask") or 0)
        if error or quality != "OK" or spread is None or abs(ask / close - 1) > .02 or abs(ask / float(quote["ask"]) - 1) > .01:
            print("BLOCK fresh execution quote"); return 2
        fresh_stop = ask * (1 - STOP_FRACTION - COST_BUFFER)
        fresh_size = proposed_shares(CAPITAL, ask, fresh_stop, 0, GROSS_CAP)
        qty = min(qty, fresh_size["proposed_shares"], math.floor(NAME_CAP / ask),
                  math.floor(max(0, GROSS_CAP - gross) / (ask * 1.001)))
        if qty < 1: return 2
        oid = app.next_order_id
        if oid < 1: raise RuntimeError("missing broker order ID")
        contract = trader.Contract()
        contract.symbol, contract.secType, contract.exchange, contract.currency = symbol,"STK","SMART","USD"
        order = trader.Order()
        order.action, order.orderType, order.tif = "BUY", "LMT", "DAY"
        order.totalQuantity, order.lmtPrice = qty, round(ask * 1.001, 2)
        order.eTradeOnly = False
        order.firmQuoteOnly = False
        order.account, order.orderRef = ACCOUNT, ORDER_REF
        done = threading.Event()
        original = app.orderStatus
        def on_status(*args):
            original(*args)
            if args[0] == oid: done.set()
        app.orderStatus = on_status
        app.placeOrder(oid, contract, order)
        if not done.wait(10):
            print("ORDER STATUS UNKNOWN", oid, "check TWS before retrying"); return 2
        for _ in range(20):
            result = app.order_results.get(oid, {})
            if result.get("status") in ("Filled", "Cancelled", "ApiCancelled", "Inactive"):
                break
            time.sleep(.25)
        result = app.order_results.get(oid,{})
        print("ORDER", oid, "BUY", qty, symbol, "limit",order.lmtPrice,"status",result)
        if result.get("status") == "Inactive":
            return 2
        if result.get("status") != "Filled":
            app.cancelOrder(oid)
            for _ in range(32):
                if app.order_results.get(oid, {}).get("status") in ("Cancelled", "ApiCancelled", "Filled"):
                    break
                time.sleep(.25)
            result = app.order_results.get(oid, {})
            print("FINAL AFTER CANCEL", oid, result)
            if result.get("status") not in ("Cancelled", "ApiCancelled", "Filled"):
                print("ORDER STATUS UNKNOWN after cancellation; inspect broker before retrying")
                return 2
        # Record intent locally, not in the public repository; fills must be separately reconciled.
        STATE.mkdir(parents=True,exist_ok=True)
        with (STATE / "intent.log").open("a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} {ORDER_REF} {oid} BUY {qty} {symbol} LMT {order.lmtPrice} {result.get('status')}\n")
        filled = int(result.get("filled") or 0)
        if filled:
            app.disconnect()
            app, current, pending = broker_snapshot(client_id=90)
            holding = current.get((ACCOUNT, symbol))
            if not holding or holding[0] != filled or pending:
                print("BLOCK fill/position reconciliation mismatch; inspect TWS")
                return 2
            record = {"timestampUtc": datetime.now(timezone.utc).isoformat(),
                      "strategy": "WYCKOFF-RISK025", "account": ACCOUNT, "symbol": symbol,
                      "side": "BUY", "quantity": filled, "orderId": oid, "orderRef": ORDER_REF,
                      "limitUsd": order.lmtPrice, "fillUsd": result.get("avgFillPrice"),
                      "brokerAvgCostUsd": holding[1], "plannedRiskUsd": CAPITAL * .0025,
                      "status": "Filled"}
            with (STATE / "trades.jsonl").open("a") as f:
                f.write(json.dumps(record) + "\n")
            print("VERIFIED_FILL", symbol, filled, result.get("avgFillPrice"), "no open orders")
        return 0
    finally:
        app.disconnect()


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol", nargs="?")
    parser.add_argument("--auto", action="store_true", help="choose one unheld long candidate from the canonical list")
    parser.add_argument("--execute",action="store_true")
    args=parser.parse_args()
    try:
        STATE.mkdir(parents=True,exist_ok=True)
        with (STATE / "entry.lock").open("a") as lock:
            try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print("SKIP another experiment entry check is running"); raise SystemExit(0)
            if not market_open(datetime.now(timezone.utc)):
                print("SKIP outside regular-session entry window"); raise SystemExit(0)
            if args.auto:
                symbol = auto_symbol()
                if not symbol:
                    print("SKIP no eligible new experiment candidate"); raise SystemExit(0)
            else:
                symbol = args.symbol
            raise SystemExit(run(symbol,args.execute))
    except Exception as exc:
        print("BLOCK",type(exc).__name__,exc)
        raise SystemExit(2)
