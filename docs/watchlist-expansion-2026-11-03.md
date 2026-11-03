# Paper watchlist expansion — 2026-11-03

Owner requested expanding the order-eligible paper ticker universe from 30 to 40 on 2026-11-03. This is a paper-account-only change; no orders were placed during the edit.

## Added names

AIG, ALL, PRU, HIG, C, USB, PNC, MPC, MS, GS. These are the ten names from the previously tested read-only research pool. They are assigned to SWING_TRADE_STOCKS at the existing $30,000 per-symbol legacy bucket value. No existing names were removed or remapped.

The discovery work established that one Alpaca REST latest-quotes call returned all 40 symbols, and the three yfinance bar intervals were available in the earlier test. That is a technical data-path test—not a valuation/fundamental certification. Vendor trailing P/E values in the Oct 30 review were explicitly unverified; issuer/SEC reconciliation, especially for bank/insurer earnings and sector concentration, remains open. On an earlier sample, ALL/HIG/PNC/GS had spreads above 4%; execution-quality and fresh-quote gates remain mandatory. Research-only scan results do not authorize orders.

## Position and risk checks

Fresh IBKR paper snapshot at 2026-11-03 10:31 Asia/Jerusalem: account DUO957759 had 17 positions and zero open orders. None of the ten new symbols was held or had an open order. Existing holdings were retained unchanged.

No sizing, exits, thresholds, or strategy caps changed. Existing paper pilot controls remain $80,000 gross per sleeve, $10,000 per name, $200 planned risk per entry, at most two new fills per day per strategy, plus fresh quote/spread, session, complete-inventory, duplicate-position/open-order and intent-reconciliation gates. Planned risk is not guaranteed maximum loss. Exposure across sleeves/legacy holdings can still be correlated; this expansion does not add capital or relax those safeguards.

## Implementation and verification
Read-only live 40-name scan at 2026-11-03 10:33 Asia/Jerusalem (US premarket) returned bars and completed in 7.8 seconds, but only 27/40 Alpaca quotes passed basic validity; those 27 were stale by about 694 minutes and wide. The remaining 13 were invalid/missing-side quotes. This is expected premarket and **none is executable**: freshness/spread gates must pass again during the US session before any candidate can trade.

- Canonical WATCHLIST: 40 unique names; existing six day-trade assignments and 34 swing assignments cover each name exactly once.
- scan_watchlist.py and the standalone read-only full-universe scanner now use the canonical 40-name list.
- README and the daily research prompt were updated. The enabled daily research job retains its 08:00 Asia/Jerusalem schedule and no-orders policy, now with a maximum of 40.
- Verification completed: 52 unit tests pass; Python syntax and diff checks pass; the read-only 40-name scan completed. Scheduled guarded paper checks remain on their existing cadence and execution gates.
