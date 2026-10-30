# Expanded ticker research — 2026-10-30 (read-only)

The canonical 30-name trading watchlist is unchanged. This is an **unapproved discovery pool**, not order authorization. Yahoo Finance screener was read during the 19:02–19:10 Israel-time session: United States region, vendor Trailing P/E 0–20, then manually narrowed below 15. Yahoo's “US” region also includes OTC, preferred shares and ADRs, so region alone is not exchange verification. Screened vendor P/E is not independently reconciled to filings; quote and earnings as-of dates need separate checks. A second stockanalysis.com screen was blocked by Cloudflare. The Chrome extension profile reported running but tab connections timed out; a managed Chromium browser reached the Yahoo screener.

## Newly observed on Yahoo public screener (preliminary only)

| Symbol | Yahoo screen P/E TTM | Approx price USD | 3-month average volume | Reason to investigate |
|---|---:|---:|---:|---|
| BRK-B | 13.58 | 546.80 | 4.385M | diversified insurer; confirm trade class and reporting |
| MU | 12.50 | 877.05 | 27.761M | semiconductors; check cyclical earnings and unusual price |
| HSBC | 11.17 | 85.49 | 1.544M | ADR bank; FX/ADR and capital adequacy |
| MS | 14.83 | 183.79 | 5.228M | broker/bank; near P/E threshold |
| GS | 13.12 | 887.78 | 2.061M | investment bank; earnings cyclicality |

JPM and BAC also appeared but are already canonical. C is additionally in the daily wider vendor sample (12.26 unverified trailing P/E there); it is not an independently confirmed screen match. The Yahoo screen includes thin OTC Chinese banks, preferred shares and BRK-A; those were **not** counted as fresh candidates. Screen volume is not a quote-quality or spread check.

## Additional names in the 2026-10-30 daily vendor sample

AIG 14.92, ALL 5.12, PRU 10.59, HIG 8.84, USB 11.80, PNC 12.16, UAL 9.63 and MPC 14.98 trailing P/E (all **unverified** vendor observations). Their approximate average daily dollar volume in that review was $202M–$919M, except none was independently checked against official issuer results today. Especially investigate ALL's low multiple for one-off earnings before acceptance. Source: [daily ticker review](ticker-review-2026-10-30.md).

## First expanded signal scan (read-only)

At 19:18 Israel time a standalone 40-name batch completed in 7.3 seconds (30 active + 10 research candidates). Candidate AIG had SHORT/NEUTRAL/NEUTRAL, 0.02% quote spread; C had LONG/NEUTRAL/NEUTRAL, 0.18% spread. ALL, HIG, PNC, MPC and GS had spreads 3.77%–10.37% and were **not actionable quotes**. PRU, USB and MS were neutral. These technical signals are not validated fundamentals or entry approvals; the extra ten are not traded.

## Expand discovery without raising active execution risk

1. Maintain a research pool of ~80–150 symbols from public screeners, with source, retrieval time, exchange/common-share verification, liquidity, vendor trailing P/E, risk/catalyst, and issuer/SEC cross-check status. Do **not** treat Yahoo screener/volume as filings proof.
2. Batch research into small groups and cache daily fundamentals; use Yahoo/yfinance only as a discovery aid, respecting rate limits and data quality. Do not make 150 per-symbol requests every 30 minutes.
3. Keep the current 30-name quote/signal cycle until quote API capacity and latency are measured; separately rank the research pool daily. Promote only a documented candidate after a complete IBKR paper position/open-order inventory, preserving held or pending-order tickers. Replacement must be unheld/unordered and approved by the daily research policy; daily review remains order-free.
4. **The 30-symbol limit is a Basic WebSocket subscription limit, not a documented REST latest-quotes limit:** Alpaca documents the REST `symbols` list without a 30-name maximum; its Basic historical API allowance is 200 requests/minute and basic real-time equity coverage is IEX-only, not consolidated. In addition, on 2026-10-30 one read-only Alpaca request for 40 unique symbols returned HTTP 200 and all 40 quote objects (zero missing). A 40-symbol Yahoo/yfinance three-timeframe batch returned bars for 40/40 daily, weekly and monthly in 3.47/1.82/1.83 seconds, respectively. This proves one small expansion is technically feasible, not that 80–150 symbols will stay fresh or within vendor rate limits. Add a separate research-only scan with completeness, timestamp and spread checks before changing any trading universe. A bigger screen does not increase each strategy's separate $80k simulated sleeve or relax the $200 planned-risk gate.

Sources: <https://docs.alpaca.markets/us/docs/about-market-data-api>, <https://docs.alpaca.markets/us/v1.1/reference/stocklatestquotes-1>, <https://docs.alpaca.markets/us/docs/historical-stock-data-1>, <https://finance.yahoo.com/research-hub/screener/equity/> (dynamic screen, observed 2026-10-30), <https://finance.yahoo.com/quote/BRK-B/>, <https://finance.yahoo.com/quote/MU/>, <https://finance.yahoo.com/quote/HSBC/>, <https://finance.yahoo.com/quote/MS/>, <https://finance.yahoo.com/quote/GS/>, <https://finance.yahoo.com/quote/C/>, and the linked daily review. No orders were placed by this research.
