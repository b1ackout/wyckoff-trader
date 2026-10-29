#!/usr/bin/env python3
"""Paper-only, position-aware exits. No new entries or automatic reversals."""
import argparse
import math
import sys
import threading
import time
from datetime import datetime, timezone, time as clock
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import trade_cycle as trader
from scan_watchlist import download_batch, fetch_quotes, quote_quality

ACCOUNT = "DUO957759"
LOSS_FRACTION = 0.08
PROFIT_FRACTION = 0.12
HOLIDAYS_2026 = {(2026, 11, 26), (2026, 12, 25)}


def exit_reason(qty, cost, close, daily=None, weekly=None, monthly=None):
    """Use a valid market price; never infer entry dates or a historical R multiple."""
    if not qty or not all(math.isfinite(x) and x > 0 for x in (cost, close)):
        return None
    signed_return = (close / cost - 1) * (1 if qty > 0 else -1)
    if signed_return <= -LOSS_FRACTION:
        return "8% adverse move from broker average cost"
    if signed_return >= PROFIT_FRACTION:
        return "12% favorable move from broker average cost"
    opposite = "SHORT" if qty > 0 else "LONG"
    if sum(signal == opposite for signal in (daily, weekly, monthly)) >= 2:
        return "two-timeframe opposite signal"
    return None


def market_open(now):
    ny = now.astimezone(ZoneInfo("America/New_York"))
    return ny.year == 2026 and ny.weekday() < 5 and (ny.year, ny.month, ny.day) not in HOLIDAYS_2026 and clock(9, 35) <= ny.time() < clock(15, 55)


def broker_snapshot(client_id=78):
    app = trader.IBKRApp()
    positions, orders, accounts = {}, {}, []
    positions_done, orders_done, accounts_done = threading.Event(), threading.Event(), threading.Event()
    def account_list(ids):
        accounts.extend(ids.split(",")); accounts_done.set()
    def position(acct, contract, qty, cost):
        if qty: positions[(acct, contract.symbol)] = (qty, cost, contract.secType, contract.currency)
    def open_order(oid, contract, order, state):
        orders[oid] = (contract.symbol, state.status)
    app.managedAccounts = account_list
    app.position = position
    app.positionEnd = positions_done.set
    app.openOrder = open_order
    app.openOrderEnd = orders_done.set
    app.connect("127.0.0.1", 7497, clientId=client_id)
    threading.Thread(target=app.run, daemon=True).start()
    for _ in range(100):
        if app.connected: break
        time.sleep(.1)
    if not app.connected or not accounts_done.wait(5) or accounts != [ACCOUNT]:
        app.disconnect(); raise RuntimeError("paper account connection/identity unavailable")
    app.reqPositions(); app.reqAllOpenOrders()
    if not positions_done.wait(15) or not orders_done.wait(15):
        app.disconnect(); raise RuntimeError("broker position/open-order inventory incomplete")
    return app, positions, orders


def submit_exit(app, symbol, qty, quote):
    """Submit at most the held shares; call only after a fresh broker snapshot and quote gate."""
    bid, ask = float(quote["bid"]), float(quote["ask"])
    action = "SELL" if qty > 0 else "BUY"
    reference = bid if qty > 0 else ask
    contract = trader.Contract()
    contract.symbol, contract.secType, contract.exchange, contract.currency = symbol, "STK", "SMART", "USD"
    order = trader.Order()
    order.action, order.orderType, order.tif = action, "LMT", "DAY"
    order.totalQuantity = abs(int(qty))
    order.lmtPrice = round(reference * (0.995 if qty > 0 else 1.005), 2)
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    order.account = ACCOUNT
    oid = app.next_order_id
    app.next_order_id += 1
    app.placeOrder(oid, contract, order)
    return oid, action, order.totalQuantity, order.lmtPrice


def run(execute=False):
    now = datetime.now(timezone.utc)
    app, positions, orders = broker_snapshot()
    try:
        print("Paper account", ACCOUNT, "positions", len(positions), "open orders", len(orders))
        if orders:
            print("BLOCK: broker open orders exist; no new exit submissions")
            return 2
        symbols = [s for (acct, s), (qty, cost, sec, currency) in positions.items()
                   if acct == ACCOUNT and sec == "STK" and currency == "USD" and s in trader.WATCHLIST]
        if not symbols: return 0
        daily = download_batch(symbols, "3mo", "1d")
        weekly = download_batch(symbols, "1y", "1wk")
        monthly = download_batch(symbols, "5y", "1mo")
        quotes, err = fetch_quotes(symbols)
        if err: print("BLOCK quotes:", err); return 2
        eligible = []
        for symbol in symbols:
            qty, cost, _, _ = positions[(ACCOUNT, symbol)]
            bars = {"daily": daily[symbol], "weekly": weekly[symbol], "monthly": monthly[symbol]}
            if not bars["daily"] or any(len(bars[tf]) < 20 for tf in bars):
                print(symbol, "SKIP: insufficient bars"); continue
            close = bars["daily"][-1]["c"]
            signal, _, tf = trader.analyze_wyckoff_multitf(symbol, quotes.get(symbol, {}), bars)
            reason = exit_reason(qty, cost, close, *(tf[x] for x in ("daily", "weekly", "monthly")))
            if not reason: continue
            quote = quotes.get(symbol, {})
            spread, quality = quote_quality(quote, datetime.now(timezone.utc))
            if quality != "OK" or spread is None:
                print(symbol, "SIGNAL", reason, "BLOCK quote:", quality); continue
            side = float(quote["bid"] if qty > 0 else quote["ask"])
            if abs(side / close - 1) > .02:
                print(symbol, "SIGNAL", reason, "BLOCK quote differs >2% from daily close"); continue
            print(symbol, "EXIT", reason, "held", int(qty), "daily close", round(close, 2),
                  "quote", quote["bid"], quote["ask"])
            eligible.append((symbol, qty))
        if not execute:
            print("DRY RUN: no orders submitted"); return 0
        if not market_open(datetime.now(timezone.utc)):
            print("SKIP: outside regular US session 09:35–15:55 ET; no orders"); return 0
        if not eligible:
            print("No executable exit signals"); return 0
        # Reconcile immediately before any order, and reject changed holdings or pending orders.
        app.disconnect()
        app, latest, pending = broker_snapshot(client_id=79)
        if pending or any(latest.get((ACCOUNT, s)) != positions.get((ACCOUNT, s)) for s, _ in eligible):
            print("BLOCK: position/order inventory changed"); return 2
        acknowledged = threading.Event()
        expected = [None]
        original_status = app.orderStatus
        def on_status(*args):
            original_status(*args)
            if args[0] == expected[0]: acknowledged.set()
        app.orderStatus = on_status
        for symbol, qty in eligible:
            if not market_open(datetime.now(timezone.utc)):
                print("BLOCK: market session ended"); return 2
            current, error = fetch_quotes([symbol])
            q = current.get(symbol, {})
            spread, quality = quote_quality(q, datetime.now(timezone.utc))
            close = daily[symbol][-1]["c"]
            if error or quality != "OK" or spread is None or abs(float(q["bid"] if qty > 0 else q["ask"]) / close - 1) > .02:
                print(symbol, "SKIP: fresh quote failed"); continue
            acknowledged.clear()
            expected[0] = app.next_order_id
            oid, action, amount, limit = submit_exit(app, symbol, qty, q)
            if not acknowledged.wait(8):
                print(symbol, "ORDER STATUS UNKNOWN", oid, action, amount, limit, "stop further submissions")
                return 2
            result = app.order_results.get(oid, {})
            print(symbol, "ORDER", oid, action, amount, limit, result)
            if result.get("status") in ("Inactive", "Cancelled", "ApiCancelled"):
                return 2
            # One ticket per invocation; reconcile again before any other exit.
            return 0
        return 0
    finally:
        app.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="allow guarded paper close orders")
    args = parser.parse_args()
    try: raise SystemExit(run(args.execute))
    except Exception as exc:
        print("BLOCK:", type(exc).__name__, exc)
        raise SystemExit(2)
