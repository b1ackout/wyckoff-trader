# Paper strategy experiments

Objective: maximize **risk-adjusted** profit, not trade count. The IBKR account is simulated; virtual sleeves are accounting constructs, not separate broker accounts. A position must have an orderRef and local entry log before attributing P&L to an experiment; legacy positions remain an unassigned baseline.

| Experiment | State | Signal | Capital model | Risk and exit | Trading frequency |
|---|---|---|---|---|---|
| WYCKOFF-RISK025 | paper pilot, long-only new entries | canonical daily/weekly/monthly Wyckoff LONG, unheld ticker | simulated $80k USD sleeve; $80k virtual gross cap; $10k/name | $200 planned loss budget, 8% invalidation plus 0.5% reserve; existing guarded manager closes at 8% adverse/12% favorable/two opposing TF | inspect each scheduled market-hours scan; never force entries |
| INTRADAY-MOMENTUM | guarded paper pilot (long-only; pending scheduled proof) | fresh completed 5-minute breakout with volume confirmation | independent simulated $80k gross, $10k/name | $200 planned risk, 2% adverse / 3% favorable / 15:15 ET close attempt; overnight residual allowed if unfilled | at most two new filled symbols/day, entry cutoff 14:30 ET; 30-minute checks |
| MEAN-REVERSION | shadow only | daily RSI/volatility pullback with trend filter | independent simulated $80k | proposed max $200 per signal, max five-day hold | daily evaluations |

Evaluation ledger (local state, not public Git): timestamp, strategy ID, symbol, signal/entry/stop, requested shares, orderRef/orderId, fill, fees/FX, exit, R multiple, holding time, maximum adverse/favorable excursion. Track rejected signals and broker outages as distinct from executed trades. Compare net P&L, drawdown, exposure, turnover, hit rate and average win/loss per sleeve after a prespecified sample; no claim of edge from a few fills.

Execution gates: only the approved paper account, no existing position or open order for the symbol, fresh uncrossed quote <=1% spread and within 2% of current bar, market-hours gate, and confirmed broker callbacks. No automatic shorts in the pilot until borrow and short-specific controls are tested. A virtual 0.25% stop risk does **not** guarantee a $200 maximum loss; gaps and the lack of a resting broker stop can exceed it. Do not convert the account's legacy positions into a new sleeve retroactively.

## Momentum promotion gate (2026-10-30)

User accepted overnight carry if a close cannot fill. The shadow scanner rejects prior-session/unfinished/stale 5-minute bars. The momentum pilot has its own tagged order intent, execution and broker-position reconciliation; its planned stop is a polling rule, not a guaranteed loss limit. Deployment still requires an end-to-end scheduled no-order test and a broker-confirmed paper order/fill before claiming the order path proven. Promotion gates:

1. Dedicated per-order orderRef and local intent/fill/exit ledger; incomplete broker executions, partial fill/cancel races or a ledger mismatch block new entries. The legacy Wyckoff manager excludes momentum-owned shares on exact broker/ledger match.
2. Independent $80k simulated gross cap, $200 planned risk per trade, $10k per-name cap and two new symbol fills/day; fresh timestamped bar/quote gates, same-session deduplication, and a second complete paper snapshot before order submission.
3. The momentum exit path attempts a close after 15:15 ET or at its price thresholds and retries an overnight residual next market session. A 30-minute scheduler and DAY limit do not guarantee flat-by-close or a maximum loss. Missing broker coverage must be reported, not interpreted as safety.
4. Mocked broker tests cover ownership, partial fills, cancel/fill races and stale quotes. Prove scheduled delivery and then a tiny actual paper fill with complete execution/position/open-order reconciliation before asserting the broker path is validated. Mean reversion remains shadow-only.

Allocation update 2026-10-30: each of Wyckoff, intraday momentum and proposed mean reversion has its own independent **$80,000 simulated USD sleeve**, not $80k total and not a transfer of real funds. Exposure caps are separate, so combined new-pilot capacity could reach $240k; inherited paper holdings remain unassigned. The 0.25% risk target is $200 planned stop-distance risk per trade, not guaranteed loss. Each order still requires fresh quotes, verified paper inventory and a strategy-specific exit.
