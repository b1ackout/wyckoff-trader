#!/usr/bin/env python3
"""Wyckoff paper-trading cycle: Alpaca quotes + multi-TF Wyckoff + IBKR TWS execution."""
import os, sys, time, logging
from datetime import datetime
from threading import Thread

# --- Alpaca credentials -----------------------------------------------------
alpaca_env = {}
with open(os.path.expanduser("~/.config/alpaca/env")) as f:
    for line in f:
        line = line.strip()
        if line.startswith("export "):
            key, val = line.replace("export ", "").split("=", 1)
            alpaca_env[key.strip()] = val.strip()

ALPACA_API_KEY = alpaca_env["ALPACA_API_KEY"]
ALPACA_SECRET_KEY = alpaca_env["ALPACA_SECRET_KEY"]
ALPACA_DATA_URL = "https://data.alpaca.markets/v2"

# --- Watchlist (P/E < 15, US only) -----------------------------------------
WATCHLIST = ["PYPL", "DHI", "EQNR", "EOG", "B", "PDD", "CVE", "UBER",
             "VZ", "CMCSA", "F", "GM", "INTC", "BAC", "WFC", "XOM",
             "CVX", "T", "JPM", "MO", "KHC", "PCG"]

DAY_TRADE_STOCKS = {"PYPL": 30000, "DHI": 30000, "UBER": 30000, "F": 30000, "GM": 30000, "INTC": 30000}
SWING_TRADE_STOCKS = {"EQNR": 30000, "EOG": 30000, "B": 30000, "PDD": 30000, "CVE": 30000,
                      "VZ": 30000, "CMCSA": 30000, "BAC": 30000, "WFC": 30000, "XOM": 30000,
                      "CVX": 30000, "T": 30000, "JPM": 30000, "MO": 30000, "KHC": 30000, "PCG": 30000}

NOTES_FILE = "/home/deck/.openclaw/workspace/wyckoff_notes.md"
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout)])
log = logging.getLogger("wyckoff")

# --- Alpaca quotes ----------------------------------------------------------
def alpaca_request(endpoint, params=None):
    import requests
    headers = {"APCA-API-KEY-ID": ALPACA_API_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY}
    url = f"{ALPACA_DATA_URL}/{endpoint}"
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        return resp.status_code, resp.json()
    except Exception as e:
        return None, {"error": str(e)}

def get_alpaca_quotes(symbols):
    quotes = {}
    for symbol in symbols:
        status, data = alpaca_request(f"stocks/{symbol}/quotes/latest")
        if status == 200 and data.get("quote"):
            q = data["quote"]
            quotes[symbol] = {"bid": q.get("bp"), "ask": q.get("ap"), "last": q.get("bp"), "timestamp": q.get("t")}
            log.info(f"  {symbol:6s} | Bid: {q.get('bp')} | Ask: {q.get('ap')}")
        else:
            log.warning(f"  {symbol:6s} | Alpaca error: {status}")
    return quotes

# --- yfinance multi-timeframe bars -----------------------------------------
def fetch_bars(symbol, period, interval):
    import yfinance as yf
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        if hist.empty:
            return []
        bars = []
        for idx, row in hist.iterrows():
            bars.append({"o": float(row["Open"]), "h": float(row["High"]), "l": float(row["Low"]),
                         "c": float(row["Close"]), "v": int(row["Volume"]), "t": str(idx)})
        return bars
    except Exception as e:
        log.error(f"  {symbol:6s} | yfinance exception ({period}/{interval}): {e}")
        return []

def fetch_all_timeframes(symbol):
    return {"daily": fetch_bars(symbol, "3mo", "1d"),
            "weekly": fetch_bars(symbol, "1y", "1wk"),
            "monthly": fetch_bars(symbol, "5y", "1mo")}

# --- Wyckoff analysis (multi-timeframe) ------------------------------------
def wyckoff_signal_for_timeframe(symbol, quote, bars, tf_name):
    if not bars or len(bars) < 20:
        return "NEUTRAL", f"Insufficient {tf_name} data ({len(bars) if bars else 0} bars)"
    closes = [b["c"] for b in bars]; highs = [b["h"] for b in bars]
    lows = [b["l"] for b in bars]; volumes = [b["v"] for b in bars]
    # Use latest bar close as reference price (yfinance 1d includes the live bar)
    current_price = closes[-1] if closes else 0
    if not current_price:
        return "NEUTRAL", "No current price"
    recent_high = max(highs[-20:]); recent_low = min(lows[-20:])
    avg_volume = sum(volumes[-20:]) / 20 if volumes else 0
    current_volume = volumes[-1] if volumes else 0
    price_near_low = current_price <= recent_low * 1.03   # widened from 2% to 3%
    volume_high = current_volume > avg_volume * 1.3 if avg_volume > 0 else False  # lowered from 1.5x
    rsi = _rsi(closes, 14)
    rsi_oversold = rsi is not None and rsi < 35
    rsi_overbought = rsi is not None and rsi > 65
    vol_divergence = _volume_divergence(closes, volumes)
    if price_near_low and (volume_high or rsi_oversold) and closes[-1] > closes[-2]:
        tag = "Spring/SOS"
        if rsi_oversold: tag += "+RSI"
        if vol_divergence: tag += "+VolDiv"
        return "LONG", f"{tf_name} {tag} near support ({recent_low:.2f})"
    price_near_high = current_price >= recent_high * 0.97
    if price_near_high and (volume_high or rsi_overbought) and closes[-1] < closes[-2]:
        tag = "Upthrust/SOW"
        if rsi_overbought: tag += "+RSI"
        return "SHORT", f"{tf_name} {tag} near resistance ({recent_high:.2f})"
    if rsi_oversold and price_near_low:
        return "LONG", f"{tf_name} RSI oversold ({rsi:.0f}) near support ({recent_low:.2f})"
    if rsi_overbought and price_near_high:
        return "SHORT", f"{tf_name} RSI overbought ({rsi:.0f}) near resistance ({recent_high:.2f})"
    return "NEUTRAL", f"{tf_name} No clear pattern (RSI={rsi:.0f})" if rsi is not None else f"{tf_name} No clear pattern"

def _rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, period + 1):
        d = closes[-period - 1 + i] - closes[-period - 2 + i]
        gains.append(max(d, 0)); losses.append(max(-d, 0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _volume_divergence(closes, volumes, n=5):
    """True if recent down bars show decreasing volume (accumulation)."""
    if len(closes) < n + 1 or len(volumes) < n + 1:
        return False
    down_bars = [i for i in range(-n, 0) if closes[i] < closes[i-1]]
    if len(down_bars) < 2:
        return False
    vols = [volumes[i] for i in down_bars]
    return vols[-1] < vols[0]

def analyze_wyckoff_multitf(symbol, quote, all_bars):
    tf_signals = {}
    for tf_name in ["daily", "weekly", "monthly"]:
        bars = all_bars.get(tf_name, [])
        signal, reason = wyckoff_signal_for_timeframe(symbol, quote, bars, tf_name)
        tf_signals[tf_name] = signal
    long_count = sum(1 for s in tf_signals.values() if s == "LONG")
    short_count = sum(1 for s in tf_signals.values() if s == "SHORT")
    # AGGRESSIVE: single timeframe is enough
    if long_count >= 1:
        tf = [k for k, v in tf_signals.items() if v == "LONG"][0]
        return "LONG", f"{tf.title()} LONG ({long_count}/3 TFs)", tf_signals
    elif short_count >= 1:
        tf = [k for k, v in tf_signals.items() if v == "SHORT"][0]
        return "SHORT", f"{tf.title()} SHORT ({short_count}/3 TFs)", tf_signals
    else:
        return "NEUTRAL", "No Wyckoff pattern across timeframes", tf_signals

# --- IBKR TWS --------------------------------------------------------------
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

class IBKRApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.connected = False
        self.next_order_id = 1
        self.account_summary = {}
        self.positions = {}
        self.order_results = {}
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        self.connected = True
        log.info(f"IBKR TWS connected — next order ID: {orderId}")
    def accountSummary(self, reqId, account, tag, value, currency):
        self.account_summary[tag] = f"{value} {currency}"
    def accountSummaryEnd(self, reqId):
        log.info("Account summary received")
    def position(self, account, contract, position, avgCost):
        self.positions[contract.symbol] = {"position": position, "avgCost": avgCost}
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        self.order_results[orderId] = {"status": status, "filled": filled, "remaining": remaining, "avgFillPrice": avgFillPrice}
        log.info(f"Order {orderId}: {status} — filled {filled}, avg price {avgFillPrice}")
    def error(self, reqId, errorCode, errorString, *args):
        if errorCode not in (2104, 2106, 2158, 2186):
            log.error(f"IBKR Error {errorCode}: {errorString}")

def connect_ibkr():
    app = IBKRApp()
    app.connect("127.0.0.1", 7497, clientId=22)
    thread = Thread(target=app.run, daemon=True)
    thread.start()
    timeout = 10
    start = time.time()
    while not app.connected and (time.time() - start) < timeout:
        time.sleep(0.1)
    if not app.connected:
        log.error("Failed to connect to IBKR TWS on port 7497")
        return None
    app.reqAccountSummary(9001, "All", "$LEDGER:ALL")
    time.sleep(2)
    app.reqPositions()
    time.sleep(2)
    return app

NOTIONAL_PER_NAME = 30000.0  # EUR per position

def place_market_order(app, symbol, notional, action, price):
    """notional is a CASH amount; price is the reference entry price."""
    if not price or price <= 0:
        log.error(f"  {symbol:6s} | no usable price — order skipped (SAFETY)")
        return None
    quantity = int(notional // price)
    if quantity < 1:
        log.error(f"  {symbol:6s} | notional {notional:.0f} < 1 share @ {price:.2f} — skipped (SAFETY)")
        return None
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.lmtPrice = round(price * 1.005, 2)   # limit 0.5% through, avoids slippage
    order.totalQuantity = quantity
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    order.tif = "DAY"
    order_id = app.next_order_id
    app.next_order_id += 1
    app.placeOrder(order_id, contract, order)
    log.info(f"Placed {action} {quantity} {symbol} @ LMT {order.lmtPrice} (orderId={order_id})")
    time.sleep(3)
    return order_id

def log_to_notes(message):
    try:
        with open(NOTES_FILE, "a") as f:
            f.write(f"\n[{datetime.now().isoformat()}] {message}\n")
    except Exception as e:
        log.error(f"Failed to write notes: {e}")

# --- Main trade cycle ------------------------------------------------------
def run_trade_cycle():
    log.info("=" * 70)
    log.info("WYCKOFF TRADE CYCLE — MULTI-TF ANALYSIS + ALPACA + IBKR EXECUTION")
    log.info("=" * 70)
    log.info("\nFetching quotes from Alpaca...")
    quotes = get_alpaca_quotes(WATCHLIST)
    if not quotes:
        log.error("No quotes received from Alpaca")
        return
    log.info("\nFetching daily/weekly/monthly bars for Wyckoff analysis...")
    all_bars = {}
    for symbol in WATCHLIST:
        all_bars[symbol] = fetch_all_timeframes(symbol)
        d, w, m = len(all_bars[symbol]["daily"]), len(all_bars[symbol]["weekly"]), len(all_bars[symbol]["monthly"])
        log.info(f"  {symbol:6s} | D:{d} W:{w} M:{m}")
    log.info("\nConnecting to IBKR TWS...")
    app = connect_ibkr()
    if not app:
        log.error("Cannot connect to IBKR TWS")
        return
    nav = app.account_summary.get("$LEDGER-NetLiquidationByCurrency", "N/A")
    cash = app.account_summary.get("$LEDGER-CashBalance", "N/A")
    log.info(f"\nAccount: NAV={nav}, Cash={cash}")
    log.info("\nWyckoff Analysis (Multi-Timeframe):")
    trades_to_place = []
    for symbol in WATCHLIST:
        q = quotes.get(symbol, {})
        bars = all_bars.get(symbol, {})
        signal, reason, tf_signals = analyze_wyckoff_multitf(symbol, q, bars)
        log.info(f"  {symbol:6s} | {signal:6s} | {reason}")
        log.info(f"           | Daily: {tf_signals.get('daily', 'N/A'):6s} | Weekly: {tf_signals.get('weekly', 'N/A'):6s} | Monthly: {tf_signals.get('monthly', 'N/A'):6s}")
        if signal == "LONG":
            if symbol in DAY_TRADE_STOCKS:
                trades_to_place.append((symbol, DAY_TRADE_STOCKS[symbol], "BUY"))
            elif symbol in SWING_TRADE_STOCKS:
                trades_to_place.append((symbol, SWING_TRADE_STOCKS[symbol], "BUY"))
    if trades_to_place:
        log.info(f"\nPlacing {len(trades_to_place)} trade(s)...")
        for symbol, qty, action in trades_to_place:
            place_market_order(app, symbol, qty, action, quotes.get(symbol, {}).get("last", 0))
            log_to_notes(f"TRADE: {action} {qty} {symbol} @ LMT — Wyckoff multi-TF signal")
    else:
        log.info("\nNo Wyckoff signals triggered — no trades placed")
    app.disconnect()
    log.info("\nTrade cycle complete")
    log.info("=" * 70)

if __name__ == "__main__":
    run_trade_cycle()
