# Wyckoff Trader — Paper Trading on IBKR TWS

Automated Wyckoff-method paper-trading bot for the Steam Deck.
- Quotes: Alpaca (free real-time US equities)
- Bars: yfinance (daily/weekly/monthly)
- Execution: IBKR TWS Classic on 127.0.0.1:7497 (paper account)

## Layout
- `src/trade_cycle.py` — single trade cycle (Alpaca quotes + multi-TF Wyckoff + IBKR orders)
- `scripts/scanner.py` — broad-universe Wyckoff pattern scanner
- `docs/notes.md` — trade-cycle log and observations

## Run
```bash
/tmp/ibapi_env/bin/python3 src/trade_cycle.py
```

## Watchlist (22 names, P/E < 15)
PYPL, DHI, EQNR, EOG, B, PDD, CVE, UBER, VZ, CMCSA, F, GM, INTC, BAC, WFC, XOM, CVX, T, JPM, MO, KHC, PCG
