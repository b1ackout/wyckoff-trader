# Paper-account monthly P&L tracking

Script: `scripts/monthly_pnl_snapshot.py`. Daily, append-only data is stored privately outside the repository at `~/.openclaw/state/wyckoff-pnl/snapshots.jsonl` with directory mode 0700 and file mode 0600. It records IBKR paper-account identity, timestamp, NetLiquidation, cash, and the account-update `$LEDGER-RealizedPnL` / `$LEDGER-UnrealizedPnL` `BASE` values, reconciled to NetLiquidation’s currency. It avoids mixing the currency-less `reqPnL` values with account-base-currency EUR. No order APIs are called.

A weekday automation is scheduled for 22:45 Asia/Jerusalem, before the owner-reported 23:00 TWS shutdown. It captures a near-close snapshot (not guaranteed exact official close), and runs silently to avoid daily channel noise. Missing snapshots are not fabricated or backfilled.

Monthly estimate = observed daily realized base-currency values plus the change in aggregate unrealized base-currency P&L from the baseline. The report separately shows the NetLiquidation change **before external cash flows** as a cross-check; deposits/withdrawals are not inferred. The estimate flags snapshot coverage gaps. IBKR `reqPnL` realized is daily, so only saved daily observations can be accumulated.

Starting baseline is established on 2026-11-03 using the account-update BASE ledger. Earlier exploratory `reqPnL` samples were in a different currency and are excluded/superseded by this baseline. Earlier month history is not reconstructed from the single live snapshot. Backfill prior months from IBKR Activity Statements/Flex reports if desired. Request a month with: `python3 scripts/monthly_pnl_snapshot.py --report YYYY-MM`.
