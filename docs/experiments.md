# Paper strategy experiments

Objective: maximize **risk-adjusted** profit, not trade count. The IBKR account is simulated; virtual sleeves are accounting constructs, not separate broker accounts. A position must have an orderRef and local entry log before attributing P&L to an experiment; legacy positions remain an unassigned baseline.

| Experiment | State | Signal | Capital model | Risk and exit | Trading frequency |
|---|---|---|---|---|---|
| WYCKOFF-RISK025 | paper pilot, long-only new entries | canonical daily/weekly/monthly Wyckoff LONG, unheld ticker | simulated $80k USD reference; $20k virtual gross cap; $2.5k/name | $200 planned loss budget, 8% invalidation plus 0.5% reserve; existing guarded manager closes at 8% adverse/12% favorable/two opposing TF | inspect each scheduled market-hours scan; never force entries |
| INTRADAY-MOMENTUM | shadow only | 5/15-minute breakout with volume confirmation | independent virtual $20k | proposed max $50 per signal, flat by close | 30-minute evaluations once data-quality test passes |
| MEAN-REVERSION | shadow only | daily RSI/volatility pullback with trend filter | independent virtual $20k | proposed max $50 per signal, max five-day hold | daily evaluations |

Evaluation ledger (local state, not public Git): timestamp, strategy ID, symbol, signal/entry/stop, requested shares, orderRef/orderId, fill, fees/FX, exit, R multiple, holding time, maximum adverse/favorable excursion. Track rejected signals and broker outages as distinct from executed trades. Compare net P&L, drawdown, exposure, turnover, hit rate and average win/loss per sleeve after a prespecified sample; no claim of edge from a few fills.

Execution gates: only the approved paper account, no existing position or open order for the symbol, fresh uncrossed quote <=1% spread and within 2% of current bar, market-hours gate, and confirmed broker callbacks. No automatic shorts in the pilot until borrow and short-specific controls are tested. A virtual 0.25% stop risk does **not** guarantee a $200 maximum loss; gaps and the lack of a resting broker stop can exceed it. Do not convert the account's legacy positions into a new sleeve retroactively.

## Momentum promotion gate (2026-10-30)

User requested paper promotion; unattended orders remain disabled because safe execution is incomplete. The shadow scanner now rejects prior-session/unfinished/stale 5-minute bars; that is only a data prerequisite. Before changing its status to paper, implement and verify all of:

1. A dedicated orderRef, broker execution/partial-fill and cancellation reconciliation, durable momentum intent/fill/exit ledger and one shared symbol-owner gate with the Wyckoff manager. If the broker and ledger disagree, no further entry or exit assumption is safe.
2. Independent $20k simulated gross cap, $50 planned risk per trade, per-name cap and daily entry limit; fresh timestamped bar and quote gates, same-session deduplication, and a second complete paper broker snapshot immediately before order submission.
3. A separately tested momentum exit path and pre-close flattening window, including missed-check recovery, pending-order resolution, verified filled/remaining shares and explicit alert/escalation when the account cannot be confirmed flat. A 30-minute agent scheduler and DAY limit order cannot guarantee flat-by-close or a maximum loss.
4. Mocked broker tests for duplicate ownership, partial fills, cancel/fill race, stale bars, failed data, missed closing run and broker outage. Prove a no-order run, then a deliberately tiny paper order with final position/open-order reconciliation before enabling recurring entries. Keep mean reversion shadow-only.
