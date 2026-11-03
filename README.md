# Wyckoff Trader — Paper Trading on IBKR TWS

Automated Wyckoff-method paper-trading bot for the Steam Deck.
- Quotes: Alpaca (free real-time US equities)
- Bars: yfinance (daily/weekly/monthly)
- Execution: IBKR TWS Classic on 127.0.0.1:7497 (paper account)

## Monthly paper-account P&L

Read-only daily snapshots are recorded privately at `~/.openclaw/state/wyckoff-pnl/snapshots.jsonl`; monthly summaries use the IBKR base-currency ledger and flag reconciliation gaps. The weekday snapshot automation is scheduled at 22:45 Asia/Jerusalem. See `docs/monthly-pnl-tracking.md` and run `python3 scripts/monthly_pnl_snapshot.py --report YYYY-MM` for a month-to-date summary. Earlier months require IBKR statement backfill.

## Layout
- `src/trade_cycle.py` — Wyckoff signal analysis and guarded paper-exit entry point (legacy unbounded entries disabled)
- `scripts/scan_watchlist.py` — batched, read-only multi-timeframe scan for all 40 watchlist names
- `scripts/manage_positions.py` — position-aware paper exits; dry-run default, `--execute` for guarded exits
- `scripts/scheduled_check.py` — scheduled scan/exit/pilot-entry wrapper; reports broker outages without disabling future scans
- `scripts/experiment_entry.py` — tagged, capped paper-only Wyckoff pilot entry (dry-run default; `--auto --execute` for guarded scheduled pilot)
- `scripts/momentum_pilot.py` — tagged, capped intraday-momentum paper entries and owned-position exits; dry-run default
- `scripts/mean_reversion_pilot.py` — tagged mean-reversion paper entry and five-day/price exits; dry-run default; scheduled guarded paper execution
- `scripts/shadow_experiments.py` — read-only momentum diagnostics and mean-reversion signals; no orders from this script
- `docs/notes.md` — trade-cycle log and observations

## Run
```bash
/home/deck/.openclaw/state/venvs/wyckoff/bin/python3 src/trade_cycle.py
/home/deck/.openclaw/state/venvs/wyckoff/bin/python3 scripts/scan_watchlist.py
```

The read-only scan batches daily, weekly, and monthly Yahoo Finance bars for the full watchlist, and retrieves Alpaca quotes in one request. This avoids the timeout caused by sequential per-symbol requests. It never places or changes orders.

## Watchlist (40 US-listed names)
PYPL, DHI, EQNR, EOG, B, PDD, CVE, UBER, VZ, CMCSA, F, GM, INTC, BAC, WFC, XOM, CVX, T, JPM, MO, KHC, PCG, BMY, CI, HPQ, TROW, TRV, CF, PHM, AIZ, AIG, ALL, PRU, HIG, C, USB, PNC, MPC, MS, GS

The ten additional paper-trading names (AIG, ALL, PRU, HIG, C, USB, PNC, MPC, MS, GS) are assigned to the swing-trade bucket at the existing $30,000 per-symbol notional. They are experimental candidates; vendor valuation and earnings data are not filing-confirmed. The daily research automation may evaluate up to 40 names and does not place orders or liquidate held positions. Existing per-strategy $80,000 gross caps, $10,000/name caps, $200 planned-risk target, quote/session/order safeguards, and daily fill caps remain unchanged.

## Exit policy (paper account only)
The position manager closes an existing stock position on an 8% adverse move, a 12% favorable move from broker average cost, or two opposing timeframe signals. These are full closes, never automatic reversals or repeated partial trims. It requires verified paper-account positions and open orders, a fresh quote with <=1% spread and within 2% of daily close, US regular session 09:35–15:55 ET, and no pending order. It submits at most one DAY limit close ticket per invocation and awaits order status. The thresholds are decision rules, not resting broker stops; gaps may exceed them. Unbounded legacy entries, time-based exits and automated earnings exits are disabled. Only the separately capped, tagged Wyckoff pilot can make new long entries.

## Paper sizing experiment
`scripts/risk_sizing.py` simulates 0.25% of a supplied USD strategy-capital figure as planned per-trade stop risk. It sizes both long and short candidates by `floor(risk_budget / abs(entry - stop))` and further limits them by remaining gross exposure capacity. The capped Wyckoff pilot uses this calculator, but its stop is a threshold checked by the recurring exit manager, not a broker stop; sector/side exposure and short borrow constraints are not implemented for additional strategies. A stop is not a guaranteed maximum loss.

## Multiple strategy tests
See `docs/experiments.md` for independent $80k simulated sleeves for Wyckoff, momentum and mean reversion. Each uses a $200 planned risk target and an $80k gross virtual cap, $10k/name and at most two new fills per day. Only unheld long candidates with current, tight quotes may be entered; legacy paper positions are not assigned to this sleeve. Verified fills and broker intents are saved under `~/.openclaw/state/wyckoff-experiments/`, never to the public repository. Intraday momentum has a separate guarded paper pilot. It attempts 2% loss, 3% profit, or pre-close exits, but an unfilled DAY order may leave overnight paper shares (accepted for this experiment). The old Wyckoff manager excludes ledger-matched momentum holdings. Mean reversion has a guarded paper entry/exit path with a five-trading-day maximum planned hold, but no resting stop; the read-only momentum signal remains diagnostic and is not a second execution path. A first momentum broker fill has not yet been demonstrated.
