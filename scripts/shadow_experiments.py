#!/usr/bin/env python3
"""Evaluate two independent signal hypotheses without any brokerage actions."""
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
import yfinance as yf

SYMBOLS = ["UBER", "PYPL", "GM", "BAC", "XOM", "CVX", "DHI", "INTC"]
STATE = Path.home() / ".openclaw/state/wyckoff-experiments"


def rsi(closes, periods=14):
    if len(closes) < periods + 1: return None
    changes = [b - a for a, b in zip(closes[-periods-1:-1], closes[-periods:])]
    gain = sum(max(0, x) for x in changes) / periods
    loss = sum(max(0, -x) for x in changes) / periods
    return 100 if loss == 0 else 100 - 100 / (1 + gain / loss)


def intraday_momentum(closes, highs, volumes):
    if len(closes) < 21 or len(highs) != len(closes) or len(volumes) != len(closes): return False
    return closes[-1] > max(highs[-13:-1]) and volumes[-1] > 1.2 * statistics.median(volumes[-21:-1])


def daily_mean_reversion(closes):
    if len(closes) < 51:return False
    recent = rsi(closes)
    return recent is not None and recent < 45 and closes[-1] > statistics.mean(closes[-50:]) and closes[-1] < closes[-2] < closes[-3]


def series(symbols, period, interval):
    data = yf.download(symbols, period=period, interval=interval, auto_adjust=False,
                       progress=False, threads=True, group_by="ticker")
    out = {}
    for symbol in symbols:
        try:
            frame = data[symbol].dropna(subset=["Close", "High", "Volume"])
            # Last intraday candle may still be forming; never trade on it.
            if interval == "5m" and len(frame) > 1: frame = frame.iloc[:-1]
            out[symbol] = {key: [float(v) for v in frame[key]] for key in ("Close", "High", "Volume")}
        except (KeyError, TypeError):out[symbol] = {}
    return out


def main():
    intraday = series(SYMBOLS,"5d","5m")
    daily = series(SYMBOLS,"6mo","1d")
    now = datetime.now(timezone.utc).isoformat()
    observations=[]
    for symbol in SYMBOLS:
        fast=intraday.get(symbol,{})
        slow=daily.get(symbol,{})
        if fast and intraday_momentum(fast["Close"],fast["High"],fast["Volume"]):
            observations.append({"at":now,"strategy":"INTRADAY-MOMENTUM","symbol":symbol,"signal":"LONG","reference":fast["Close"][-1],"status":"shadow signal, no order"})
        if slow and daily_mean_reversion(slow["Close"]):
            observations.append({"at":now,"strategy":"MEAN-REVERSION","symbol":symbol,"signal":"LONG","reference":slow["Close"][-1],"status":"shadow signal, no order"})
    STATE.mkdir(parents=True,exist_ok=True)
    if observations:
        with (STATE / "shadow-signals.jsonl").open("a") as f:
            for row in observations:f.write(json.dumps(row)+"\n")
    print("SHADOW",len(SYMBOLS),"symbols",len(observations),"signals; no broker orders")
    for row in observations:print(row["strategy"],row["symbol"],"LONG",round(row["reference"],2))

if __name__ == "__main__":main()
