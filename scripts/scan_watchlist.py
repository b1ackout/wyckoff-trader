#!/usr/bin/env python3
"""Read-only batch Wyckoff scan for the canonical paper-trading watchlist."""
import io, logging, math, sys, time, warnings
from contextlib import redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import trade_cycle as trader
import yfinance as yf
warnings.simplefilter("ignore")
logging.getLogger("yfinance").setLevel(logging.CRITICAL)


def download_batch(symbols, period, interval):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with redirect_stderr(io.StringIO()):
            frame = yf.download(tickers=" ".join(symbols), period=period, interval=interval,
                                group_by="ticker", auto_adjust=False, progress=False,
                                threads=True, timeout=18, actions=False)
    result = {s: [] for s in symbols}
    if frame is None or frame.empty:
        return result
    for symbol in symbols:
        try:
            if getattr(frame.columns, "nlevels", 1) > 1:
                if symbol in frame.columns.get_level_values(0):
                    sub = frame[symbol]
                elif symbol in frame.columns.get_level_values(1):
                    sub = frame.xs(symbol, axis=1, level=1)
                else:
                    continue
            else:
                sub = frame
            required = ("Open", "High", "Low", "Close", "Volume")
            if any(col not in sub.columns for col in required):
                continue
            bars = []
            for idx, row in sub.iterrows():
                vals = [row[col] for col in required]
                if any(not math.isfinite(float(v)) for v in vals[:4]):
                    continue
                volume = int(vals[4]) if math.isfinite(float(vals[4])) else 0
                bars.append({"o": float(vals[0]), "h": float(vals[1]), "l": float(vals[2]),
                             "c": float(vals[3]), "v": max(0, volume),
                             "t": idx.isoformat() if hasattr(idx, "isoformat") else str(idx)})
            result[symbol] = bars
        except Exception as exc:
            print(f"DATA_ERROR {symbol} {interval}: {type(exc).__name__}: {exc}")
    return result


def fetch_quotes(symbols):
    status, payload = trader.alpaca_request("stocks/quotes/latest", {"symbols": ",".join(symbols)})
    if status != 200 or not isinstance(payload, dict):
        return {}, f"Alpaca bulk quote request failed ({status})"
    raw = payload.get("quotes", {})
    quotes = {s: {"bid": q.get("bp"), "ask": q.get("ap"), "last": q.get("bp"), "timestamp": q.get("t")}
              for s, q in raw.items() if isinstance(q, dict)}
    return quotes, None


def quote_quality(quote, now):
    if not quote:
        return None, "missing quote"
    try:
        bid, ask = float(quote.get("bid")), float(quote.get("ask"))
    except (TypeError, ValueError):
        return None, "missing bid/ask"
    if bid <= 0 or ask <= 0 or ask < bid:
        return None, f"invalid bid/ask {bid:g}/{ask:g}"
    spread = (ask - bid) / ((ask + bid) / 2)
    caveats = []
    stamp = quote.get("timestamp")
    try:
        parsed = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        age_min = (now - parsed.astimezone(timezone.utc)).total_seconds() / 60
        if age_min > 15:
            caveats.append(f"stale {age_min:.0f}m")
    except (TypeError, ValueError):
        caveats.append("missing/unparseable timestamp")
    if spread > 0.01:
        caveats.append(f"wide {spread:.2%}")
    return spread, ", ".join(caveats) if caveats else "OK"


def main():
    symbols = list(trader.WATCHLIST)
    started = time.monotonic()
    errors = []
    try:
        daily = download_batch(symbols, "3mo", "1d")
    except Exception as exc:
        daily = {s: [] for s in symbols}; errors.append(f"daily batch: {type(exc).__name__}: {exc}")
    try:
        weekly = download_batch(symbols, "1y", "1wk")
    except Exception as exc:
        weekly = {s: [] for s in symbols}; errors.append(f"weekly batch: {type(exc).__name__}: {exc}")
    try:
        monthly = download_batch(symbols, "5y", "1mo")
    except Exception as exc:
        monthly = {s: [] for s in symbols}; errors.append(f"monthly batch: {type(exc).__name__}: {exc}")
    quotes, quote_error = fetch_quotes(symbols)
    signals, neutral, missing, caveats = [], [], [], []
    now_utc = datetime.now(timezone.utc)
    valid_quotes = stale_quotes = wide_quotes = 0
    for symbol in symbols:
        bars = {"daily": daily[symbol], "weekly": weekly[symbol], "monthly": monthly[symbol]}
        if not any(bars.values()):
            missing.append(symbol)
            continue
        signal, reason, tf_signals = trader.analyze_wyckoff_multitf(symbol, quotes.get(symbol, {}), bars)
        quote = quotes.get(symbol, {})
        spread, quality = quote_quality(quote, now_utc)
        if spread is not None:
            valid_quotes += 1
            wide_quotes += int(spread > 0.01)
            try:
                stamp = datetime.fromisoformat(str(quote.get("timestamp")).replace("Z", "+00:00"))
                stale_quotes += int((now_utc - stamp.astimezone(timezone.utc)).total_seconds() > 900)
            except (TypeError, ValueError):
                pass
        if signal == "NEUTRAL":
            neutral.append(symbol)
        else:
            close = bars["daily"][-1]["c"] if bars["daily"] else None
            directions = "/".join(tf_signals.get(tf, "NA") for tf in ("daily", "weekly", "monthly"))
            line = f"{symbol} {signal} ({directions}); daily close {close:.2f}" if close is not None else f"{symbol} {signal} ({directions}); no daily close"
            if quality != "OK":
                line += f"; quote {quote.get('bid')}/{quote.get('ask')}, {quality}"
                caveats.append(symbol)
            signals.append(line)
    local_now = datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M %Z")
    print(f"Wyckoff read-only scan — {local_now}")
    print(f"Universe: {len(symbols)} tickers; three batched timeframes completed in {time.monotonic()-started:.1f}s")
    print("Signals:")
    for line in signals:
        print(f"• {line}")
    if not signals:
        print("None")
    if neutral:
        print("Neutral:", ", ".join(neutral))
    if missing:
        print("No bar data:", ", ".join(missing))
    for error in errors:
        print("DATA_ERROR:", error)
    if quote_error:
        print("QUOTE_ERROR:", quote_error)
    print(f"Quote quality: {valid_quotes}/{len(symbols)} valid; {stale_quotes} stale (>15m); {wide_quotes} wide (>1%).")
    if caveats:
        print("Signal quote caveats:", ", ".join(caveats))
    print("P/E was not reverified. No orders were placed, modified, or canceled.")
    return 2 if len(missing) == len(symbols) else 0


if __name__ == "__main__":
    raise SystemExit(main())
