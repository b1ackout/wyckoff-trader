# Wyckoff Trader — Paper Trading on IBKR TWS

Automated Wyckoff-method paper-trading bot for the Steam Deck.
- Quotes: Alpaca (free real-time US equities)
- Bars: yfinance (daily/weekly/monthly)
- Execution: IBKR TWS Classic on 127.0.0.1:7497 (paper account)

## Layout
- `src/trade_cycle.py` — single trade cycle (Alpaca quotes + multi-TF Wyckoff + IBKR orders)
- `scripts/scan_watchlist.py` — batched, read-only multi-timeframe scan for all 30 watchlist names
- `docs/notes.md` — trade-cycle log and observations

## Run
```bash
/home/deck/.openclaw/state/venvs/wyckoff/bin/python3 src/trade_cycle.py
/home/deck/.openclaw/state/venvs/wyckoff/bin/python3 scripts/scan_watchlist.py
```

The read-only scan batches daily, weekly, and monthly Yahoo Finance bars for the full watchlist, and retrieves Alpaca quotes in one request. This avoids the timeout caused by sequential per-symbol requests. It never places or changes orders.

## Watchlist (30 US-listed names)
PYPL, DHI, EQNR, EOG, B, PDD, CVE, UBER, VZ, CMCSA, F, GM, INTC, BAC, WFC, XOM, CVX, T, JPM, MO, KHC, PCG, BMY, CI, HPQ, TROW, TRV, CF, PHM, AIZ

The eight October 2026 research additions are assigned to the swing-trade bucket at the existing $30,000 per-symbol notional. Screening details, current valuation snapshot, source links, and risks are in `docs/ticker-review-2026-10-27.md`. The daily research automation is intended to re-evaluate this list and keep it at or below 30; it does not place orders or liquidate held positions.
