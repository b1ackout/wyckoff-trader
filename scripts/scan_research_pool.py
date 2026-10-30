#!/usr/bin/env python3
"""Read-only 40-symbol discovery scan; never modifies the executable 30-name list."""
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import trade_cycle as trader
from scan_watchlist import download_batch, fetch_quotes, quote_quality

CANDIDATES = ('AIG', 'ALL', 'PRU', 'HIG', 'C', 'USB', 'PNC', 'MPC', 'MS', 'GS')


def universe():
    names = list(dict.fromkeys([*trader.WATCHLIST, *CANDIDATES]))
    if len(names) != len(trader.WATCHLIST) + len(CANDIDATES):
        raise RuntimeError('research pool unexpectedly overlaps active watchlist')
    return names


def run():
    names = universe()
    started = time.monotonic()
    data = {label: download_batch(names, period, interval) for label, period, interval in
            (('daily','3mo','1d'),('weekly','1y','1wk'),('monthly','5y','1mo'))}
    quotes, error = fetch_quotes(names)
    if error or len(quotes) != len(names) or set(quotes) != set(names):
        print('RESEARCH_DATA_INCOMPLETE', error or 'missing quote symbols')
        return 2
    print('READ-ONLY RESEARCH', datetime.now(timezone.utc).isoformat(),
          'names', len(names), 'active', len(trader.WATCHLIST), 'new candidates', len(CANDIDATES))
    print('Three bar timeframes and quote batch seconds', round(time.monotonic() - started, 1))
    missing = []
    for symbol in CANDIDATES:
        bars = {tf: data[tf].get(symbol, []) for tf in data}
        if any(len(bars[tf]) < 20 for tf in bars):
            missing.append(symbol)
            continue
        q = quotes[symbol]
        spread, quality = quote_quality(q, datetime.now(timezone.utc))
        signal, reason, frames = trader.analyze_wyckoff_multitf(symbol, q, bars)
        print(symbol, signal, 'timeframes', '/'.join(frames.get(x,'?') for x in ('daily','weekly','monthly')),
              'quote', quality, 'spread_pct', round(spread * 100, 2) if spread is not None else 'NA')
    if missing: print('INSUFFICIENT_BARS', ','.join(missing))
    print('RESEARCH ONLY: vendor valuation and issuer filings NOT checked; no orders; no additions to WATCHLIST')
    return 2 if missing else 0


if __name__ == '__main__':
    raise SystemExit(run())
