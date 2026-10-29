# Wyckoff Trader — Paper Trading on IBKR TWS

Automated Wyckoff-method paper-trading bot for the Steam Deck.
- Quotes: Alpaca (free real-time US equities)
- Bars: yfinance (daily/weekly/monthly)
- Execution: IBKR TWS Classic on 127.0.0.1:7497 (paper account)

## Layout
- `src/trade_cycle.py` — Wyckoff signal analysis and guarded paper-exit entry point (new entries disabled)
- `scripts/scan_watchlist.py` — batched, read-only multi-timeframe scan for all 30 watchlist names
- `scripts/manage_positions.py` — position-aware paper exits; dry-run default, `--execute` for guarded exits
- `scripts/scheduled_check.py` — scheduled scan/exit wrapper; reports broker outages without disabling future scans
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

## Exit policy (paper account only)
The position manager closes an existing stock position on an 8% adverse move, a 12% favorable move from broker average cost, or two opposing timeframe signals. These are full closes, never automatic reversals or repeated partial trims. It requires verified paper-account positions and open orders, a fresh quote with <=1% spread and within 2% of daily close, US regular session 09:35–15:55 ET, and no pending order. It submits at most one DAY limit close ticket per invocation and awaits order status. The thresholds are decision rules, not resting broker stops; gaps may exceed them. New entries, time-based exits and automated earnings exits are disabled pending approved risk caps and reliable entry/event metadata.

## Paper sizing experiment
`scripts/risk_sizing.py` simulates 0.25% of a supplied USD strategy-capital figure as planned per-trade stop risk. It sizes both long and short candidates by `floor(risk_budget / abs(entry - stop))` and further limits them by remaining gross exposure capacity. This calculator is deliberately not connected to order placement: strategy-owned holdings, the aggregate cap, stop placement, sector/side exposure, slippage and short borrow constraints must be reconciled before new entries can be enabled. A stop is not a guaranteed maximum loss.
