# Wyckoff Method Notes — Learning Log

**Project:** Wyckoff-based trading, US market, low P/E filter
**Account:** IBKR Paper U23339441
**Capital:** €30K day trades + €30K swing holds
**Timeframe:** 30 days
**Started:** 2026-10-21

## Wyckoff Method Basics (researched)

### Core Concepts

**1. The Composite Operator**
The market is driven by a large, intelligent operator (institutional players) who accumulate positions before markup and distribute before markdown. Retail traders should identify where the Composite Operator is operating and trade in the same direction.

**2. The Three Laws**
- **Law of Supply and Demand:** Price rises when demand > supply; falls when supply > demand. Tape reading (volume/price action) reveals the balance.
- **Law of Cause and Effect:** A cause (accumulation/distribution within a trading range) produces an effect (trend move). The width of the trading range estimates the potential move size.
- **Law of Effort vs Result:** Volume (effort) vs price movement (result). Divergence between effort and result signals a potential reversal (e.g., high volume on an up-bar that fails to close higher = weakness).

**3. Market Cycle Phases**
- **Accumulation:** Smart money buys at wholesale prices after a markdown. Signs: narrowing price spread, decreasing volume on down moves, springs, SOS.
- **Markup:** Uptrend phase. Buy on pullbacks to support. Signs: higher highs/higher lows, rising volume on advances.
- **Distribution:** Smart money sells at retail prices after a markup. Signs: upthrusts, SOW, decreasing volume on rallies.
- **Markdown:** Downtrend phase. Sell short or stay out. Signs: lower highs/lower lows, heavy volume on declines.

**4. Five-Step Approach to Stock Selection**
1. Determine the present and probable future position of the general market (indexes).
2. Select stocks in harmony with the trend (strong stocks in uptrend, weak in downtrend).
3. Select stocks with a "cause" that justifies trading (building a trading range with measurable width).
4. Determine each stock's readiness to move (spring, upthrust, SOS, SOW).
5. Time your commitment with a turn in the general market index.

### Key Patterns to Spot
- **Spring:** Price briefly drops below support then quickly reverses — shakeout of weak holders before markup.
- **Upthrust:** Price briefly breaks above resistance then reverses — trap for breakout buyers before markdown.
- **Sign of Strength (SOS):** Up-bar on increased volume closing near high — buying demand entering.
- **Sign of Weakness (SOW):** Down-bar on increased volume closing near low — selling supply entering.
- **Buying Climax:** Heavy buying at top of rally, often on news — distribution begins.
- **Selling Climax:** Heavy panic selling at bottom of decline — absorption phase, potential accumulation starts.
- **Secondary Test:** Return to test the high/low of a climactic move on lighter volume.
- **Last Point of Density (LPSD/LPSY):** Final dense area of trading before a major move — confirmation of trend direction.

### How to Apply Wyckoff to Low P/E US Stocks

**Step 1 — Market Context (Index Analysis)**
- Check S&P 500, Nasdaq, Dow Jones on daily/weekly charts
- Are we in Accumulation, Markup, Distribution, or Markdown?
- Look for springs/SOS on indexes before buying individual stocks

**Step 2 — Select Stocks in Harmony with Trend**
- In Markup: Look for leading stocks with relative strength
- In Accumulation: Look for stocks building bases at support
- Filter: Low P/E relative to sector peers

**Step 3 — Identify "Cause" (Trading Range)**
- Stock must have a measurable trading range (accumulation/distribution zone)
- Width of range = estimated move size (Law of Cause and Effect)
- Look for LPSD/LPSY at the edge of the range

**Step 4 — Readiness to Move**
- Spring with SOS = ready for long
- Upthrust with SOW = ready for short
- Volume divergence: Effort vs Result check

**Step 5 — Entry Timing**
- Enter on breakout from trading range with volume confirmation
- Exit on SOW or at measured move target from range width

### Day Trade vs Swing Hold Criteria

| Criteria | Day Trades (€30K) | Swing Holds (€30K) |
|---|---|---|
| Timeframe | Intraday (5m-1h charts) | Daily/Weekly charts |
| Hold time | Minutes to hours | Days to weeks |
| Wyckoff phase focus | Markup/Markdown intraday swings | Accumulation/Distribution ranges |
| Target | Quick scalp on SOS/SOW | Full measured move from range |
| P/E filter | Less critical (momentum) | More critical (value + Wyckoff) |

### Wyckoff Check Results — 2026-10-21 (cron run #3) [historical]

**All 7 watchlist stocks pass P/E < 15 filter.** No P/E below 5 (no value-trap flags). P/E refreshed via web sources (financecharts, macrotrends, companiesmarketcap, public.com, wisesheets). Technical analysis carried over from prior check.

| Stock | P/E | Sector | Price | Wyckoff Phase | Signal | Action |
|---|---|---|---|---|---|---|
| PYPL | 10.78 | Financials | ~$57 | Accum/Support test | **Spring/SOS at support** | LONG setup — bounced at Prior Day Low / 50 SMA / 10 SMA cluster on heavy volume (2.28x avg), rose 1.11% Oct 20. Day trade candidate (€30K bucket). |
| DHI | 13.04–13.25 | Consumer Disc. | $140.17 | Transition | No clear signal | Watchlist only — volume quiet (0.71x avg). Remove from active watchlist until volume confirms. |
| EOG | 11.2–12.30 | Energy | $157.91 | Markup/Resistance | Resistance test | At 52-week high $158.37, rejected Oct 19. Narrow range (0.74x ATR). Watch for upthrust at resistance or confirmed breakout. |
| EQNR | 11.57–12.48 | Energy | $45.76 | Markup | Strong uptrend | Above SMA 50 ($43.05) and SMA 200 ($36.64). RSI 69.7, MACD 0.89 bullish. Wait for pullback to SMA 50 for Spring/SOS entry. |
| B (Barrick) | 10.40–13.8 | Materials | ~$40 | Markdown/Distrib | Bearish | Summary Bearish (4 bullish, 12 bearish, 10 neutral). MAs Strongly Bearish. RSI 46.59, MACD -0.64. Avoid longs. |
| PDD | 8.52–8.98 | Consumer Disc. | ~$81 | Accumulation base | Mixed / Base building | Price below SMA 50/100/200. RSI 55.01, MACD 0.25 bullish. P/E 8.52–8.98 — above value-trap threshold, monitor. Watch for Spring at support. |
| CVE | 12.25–12.85 | Energy | ~$32 | Markup | Strong uptrend | Strongly Bullish (17/26). Above ALL MAs (SMA 10–200). RSI 59.01 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Actionable setups (10-21):**
1. **PYPL — Long (Spring/SOS at support):** Only immediate actionable setup. Classic Spring/SOS structure at support cluster on heavy volume. Day trade candidate (€30K bucket).
2. **EQNR — Watch for pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Set alert for Spring/SOS on retest of 50-day MA.
3. **CVE — Watch for pullback to support:** Strongly bullish markup, not extended (RSI 59). Set alert for Spring/SOS on first meaningful pullback.
4. **EOG — Watch resistance at $158.37 (52-week high):** Rejected Oct 19. If upthrust (break above then reverse) → avoid/short. If breakout with volume → long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring before considering.
6. **PDD — Watch for Spring in base:** Only consider on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

---

### Wyckoff Check Results — 2026-10-22 (cron run #4)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5). Fresh P/E pulled via web_search (financecharts, macrotrends, companiesmarketcap, public.com). IBKR brokerage connection still stuck — P/E not yet verified on IBKR Fundamentals tab. Fresh intraday/daily chart data unavailable this run (no price feed), so Wyckoff technical signals carry over from 10-21; no new Spring/SOS or Upthrust/SOW confirmed today.

| Stock | P/E (fresh, 10-22) | Sector | P/E Pass <15 | Wyckoff Signal (carryover) | Action |
|---|---|---|---|---|---|
| PYPL | 10.79 (financecharts, 10-21) / 10.80 (public, 10-20) / 10.7 (companiesmarketcap) | Financials | ✅ | **Spring/SOS at support** | **LONG setup** — only actionable setup. Heavy volume bounce at support cluster (Prior Day Low / 50 SMA / 10 SMA). Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation. |
| DHI | 13.25 (financecharts, 10-16) / 13.04 (macrotrends, 10-1) | Consumer Disc. | ✅ | No clear signal | Watchlist only — volume quiet (0.71x avg). Hold off until volume confirms. |
| EOG | 12.29 (financecharts, 10-21) / 12.26 (public, 10-19) / 12.27 (wallstsmart) | Energy | ✅ | Resistance test / upthrust watch | At 52-week high ~$158.37, rejected 10-19. Watch for upthrust (break above then reverse → avoid/short) or confirmed breakout with volume → long. |
| EQNR | 12.46 (financecharts, 10-21) / 11.47 (macrotrends, 10-20) / 12.48 (trendonify, 10-20) | Energy | ✅ | Strong uptrend, not extended | Above SMA 50 & 200. RSI 69.7 (carryover). Wait for pullback to SMA 50 (~$43) for Spring/SOS entry. Not an entry here. |
| B (Barrick) | 13.8 (companiesmarketcap, 10-2026) / 13.8459 (companiesmarketcap) / 10.40 (public, 10-19) | Materials | ✅ | Bearish (markdown/distrib) | Avoid longs. Strongly bearish MAs, RSI 46.59, MACD -0.64 (carryover). Wait for selling climax or Spring before considering. |
| PDD | 8.96 (macrotrends, 10-19) / 8.52 (companiesmarketcap) / 8.98 (public, 10-16) | Consumer Disc. | ✅ | Base building / Spring watch | Price below SMA 50/100/200 (carryover). RSI 55.01, MACD 0.25 bullish. P/E well above value-trap threshold of 5. Watch for confirmed Spring/SOS at support. |
| CVE | 12.72 (financecharts, 10-21) / 12.70 (public, 10-20) / 12.25 (companiesmarketcap) | Energy | ✅ | Strong uptrend, pullback watch | Strongly bullish (17/26), above all MAs (carryover). RSI 59 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Actionable setups (10-22):**
1. **PYPL — Long (Spring/SOS at support):** Only immediate actionable setup. Classic Spring/SOS at support cluster on heavy volume. Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation with volume.
2. **EQNR — Watch pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Alert on retest of 50-day MA for Spring/SOS.
3. **CVE — Watch pullback to support:** Strongly bullish markup, not extended (RSI 59). Alert on first meaningful pullback for Spring/SOS.
4. **EOG — Watch resistance ~$158.37 (52-week high):** Rejected 10-19. Upthrust = avoid/short; breakout with volume = long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring.
6. **PDD — Watch for Spring in base:** Only on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

**Next steps:**
- Set price alerts: EQNR pullback to ~$43; CVE pullback to support; EOG breakout/upthrust at ~$158.37
- PYPL is the only immediate actionable setup (long on Spring/SOS confirmation)
- Verify P/E on IBKR Fundamentals tab before executing (brokerage connection still stuck)
- Refresh technical chart data next run to confirm/no-new Spring/SOS or Upthrust/SOW

### Wyckoff Check Results — 2026-10-22 (cron run #5)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus). Fresh P/E pulled via web_search. IBKR brokerage connection still stuck — P/E not yet verified on IBKR Fundamentals tab. No fresh price/chart feed this run, so Wyckoff technical signals carry over from 10-21; no new Spring/SOS or Upthrust/SOW confirmed today.

| Stock | P/E (fresh, 10-22) | Sector | P/E Pass <15 | Wyckoff Signal (carryover) | Action |
|---|---|---|---|---|---|
| PYPL | 10.79 (financecharts, 10-21) / 10.80 (public) / 10.7 (companiesmarketcap) / 10.6× (stockrow, 10-16) | Financials | ✅ | **Spring/SOS at support** | **LONG setup** — only actionable setup. Heavy volume bounce at support cluster (Prior Day Low / 50 SMA / 10 SMA). Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation with volume. |
| DHI | 13.21 (financecharts, 10-21) / 13.25 (financecharts, 10-16) / 13.04 (macrotrends, 10-1) | Consumer Disc. | ✅ | No clear signal | Watchlist only — volume quiet (0.71x avg). Hold off until volume confirms. |
| EOG | 12.29 (financecharts, 10-21) / 12.26 (public, 10-19) / 11.2× (stockrow, 10-6) | Energy | ✅ | Resistance test / upthrust watch | At 52-week high ~$158.37, rejected 10-19. Watch for upthrust (break above then reverse → avoid/short) or confirmed breakout with volume → long. |
| EQNR | 12.46 (financecharts, 10-21) / 11.47 (macrotrends, 10-20) / 12.48 (trendonify, 10-20) / 12.41 (public, 10-20) | Energy | ✅ | Strong uptrend, not extended | Above SMA 50 & 200. RSI 69.7 (carryover). Wait for pullback to SMA 50 (~$43) for Spring/SOS entry. Not an entry here. |
| B (Barrick) | 13.8 (companiesmarketcap) / 10.45 (trendonify, 10-21) / 13.7x (investing.com) | Materials | ✅ | Bearish (markdown/distrib) | Avoid longs. Strongly bearish MAs, RSI 46.59, MACD -0.64 (carryover). Wait for selling climax or Spring before considering. |
| PDD | 8.96 (macrotrends, 10-19) / 8.52 (companiesmarketcap) / 9.05 (public, 10-20) | Consumer Disc. | ✅ | Base building / Spring watch | Price below SMA 50/100/200 (carryover). RSI 55.01, MACD 0.25 bullish. P/E well above value-trap threshold of 5. Watch for confirmed Spring/SOS at support. (Note: financecharts shows 1.22 — data discrepancy; consensus ~8.5-9.05.) |
| CVE | 12.72 (financecharts, 10-21) / 12.70 (public, 10-20) / 12.25 (companiesmarketcap) / 12.85 (wisesheets, 10-21) | Energy | ✅ | Strong uptrend, pullback watch | Strongly bullish (17/26), above all MAs (carryover). RSI 59 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Actionable setups (10-22):**
1. **PYPL — Long (Spring/SOS at support):** Only immediate actionable setup. Classic Spring/SOS at support cluster on heavy volume. Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation with volume.
2. **EQNR — Watch pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Alert on retest of 50-day MA for Spring/SOS.
3. **CVE — Watch pullback to support:** Strongly bullish markup, not extended (RSI 59). Alert on first meaningful pullback for Spring/SOS.
4. **EOG — Watch resistance ~$158.37 (52-week high):** Rejected 10-19. Upthrust = avoid/short; breakout with volume = long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring.
6. **PDD — Watch for Spring in base:** Only on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

**Blocker:** IBKR brokerage connection stuck; no fresh intraday/daily price feed this run. Wyckoff signals cannot be newly confirmed.

---

### Wyckoff Check Results — 2026-10-22 (cron run #6)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus; PDD financecharts 1.22 is a data error — consensus ~8.5–9.05). Fresh P/E pulled via web_search (financecharts, macrotrends, companiesmarketcap, public.com). IBKR brokerage connection still stuck — P/E not yet verified on IBKR Fundamentals tab. No fresh price/chart feed this run, so Wyckoff technical signals carry over from 10-21; no new Spring/SOS or Upthrust/SOW confirmed today.

| Stock | P/E (fresh, 10-22) | Sector | P/E Pass <15 | Wyckoff Signal (carryover) | Action |
|---|---|---|---|---|---|
| PYPL | 10.79 (financecharts, 10-21) / 10.80 (public) / 10.7 (companiesmarketcap) / 10.6× (stockrow, 10-16) | Financials | ✅ | **Spring/SOS at support** | **LONG setup** — only actionable setup. Heavy volume bounce at support cluster (Prior Day Low / 50 SMA / 10 SMA). Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation with volume. |
| DHI | 13.21 (financecharts, 10-21) / 13.25 (financecharts, 10-16) / 13.04 (macrotrends, 10-1) | Consumer Disc. | ✅ | No clear signal | Watchlist only — volume quiet (0.71x avg). Hold off until volume confirms. |
| EOG | 12.29 (financecharts, 10-21) / 12.26 (public, 10-19) / 11.2× (stockrow, 10-6) | Energy | ✅ | Resistance test / upthrust watch | At 52-week high ~$158.37, rejected 10-19. Watch for upthrust (break above then reverse → avoid/short) or confirmed breakout with volume → long. |
| EQNR | 12.46 (financecharts, 10-21) / 11.47 (macrotrends, 10-20) / 12.48 (trendonify, 10-20) / 12.41 (public, 10-20) | Energy | ✅ | Strong uptrend, not extended | Above SMA 50 & 200. RSI 69.7 (carryover). Wait for pullback to SMA 50 (~$43) for Spring/SOS entry. Not an entry here. |
| B (Barrick) | 13.96 (companiesmarketcap, Oct 2026) / 13.7x (investing.com) | Materials | ✅ | Bearish (markdown/distrib) | Avoid longs. Strongly bearish MAs, RSI 46.59, MACD -0.64 (carryover). Wait for selling climax or Spring before considering. |
| PDD | 8.52 (companiesmarketcap, Oct 2026) / 8.96 (macrotrends, 10-19) / 9.05 (public, 10-20) | Consumer Disc. | ✅ | Base building / Spring watch | Price below SMA 50/100/200 (carryover). RSI 55.01, MACD 0.25 bullish. P/E well above value-trap threshold of 5. Watch for confirmed Spring/SOS at support. (Note: financecharts shows 1.22 — data discrepancy; consensus ~8.5-9.05.) |
| CVE | 12.72 (financecharts, 10-21) / 12.70 (public, 10-20) / 12.25 (companiesmarketcap) / 12.85 (wisesheets, 10-21) | Energy | ✅ | Strong uptrend, pullback watch | Strongly bullish (17/26), above all MAs (carryover). RSI 59 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Actionable setups (10-22):**
1. **PYPL — Long (Spring/SOS at support):** Only immediate actionable setup. Classic Spring/SOS at support cluster on heavy volume. Day trade candidate (€30K bucket). Re-enter only on fresh SOS confirmation with volume.
2. **EQNR — Watch pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Alert on retest of 50-day MA for Spring/SOS.
3. **CVE — Watch pullback to support:** Strongly bullish markup, not extended (RSI 59). Alert on first meaningful pullback for Spring/SOS.
4. **EOG — Watch resistance ~$158.37 (52-week high):** Rejected 10-19. Upthrust = avoid/short; breakout with volume = long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring.
6. **PDD — Watch for Spring in base:** Only on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

**Blocker:** IBKR brokerage connection stuck; no fresh intraday/daily price feed this run. Wyckoff signals cannot be newly confirmed.

### Wyckoff Check Results — 2026-10-22 (cron run #8)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus; PDD financecharts 1.22 is a known data error — consensus ~8.5–9.05). Fresh P/E pulled via web_search (financecharts, macrotrends, companiesmarketcap, public.com, fullratio, ycharts, wallstsmart, stockrow). IBKR brokerage connection still stuck — P/E not yet verified on IBKR Fundamentals tab. US market open (13:17 UTC ≈ 9:17 AM EDT). No fresh intraday/volume feed this run beyond PYPL quote ($57.14, tickzen). Wyckoff technical signals carry over from 10-21; no new Spring/SOS or Upthrust/SOW confirmed today.

| Stock | P/E (fresh, 10-22) | Sector | Price | P/E Pass <15 | Wyckoff Signal | Action |
|---|---|---|---|---|---|---|
| PYPL | 10.79 (financecharts 10-21) / 10.80 (public 10-20) / 10.7 (companiesmarketcap) / 10.73 (fullratio 10-21) / 10.81 (ycharts 10-21) / 10.6× (stockrow 10-16) | Financials | ~$57.14 (tickzen) | ✅ | **Spring/SOS played out** — bounced Oct 20 at support cluster on heavy volume, now above 50 SMA ($56.03). RSI 58.5, MACD 0.53 bullish. | Not an immediate entry at $57.14 — wait for pullback to ~$56 support for fresh SOS confirmation before entering long (€30K day trade bucket). |
| DHI | 13.21 (financecharts 10-21) / 13.04 (macrotrends 10-1) / 13.2 (stockrow 10-16) / 13.34 (public 10-20) | Consumer Disc. | ~$136.13 | ✅ | No clear signal | Watchlist only — volume quiet (0.71x avg). Hold off until volume confirms. |
| EOG | 12.29 (financecharts 10-21) / 12.26 (public 10-19) / 11.2× (stockrow 10-6) | Energy | ~$157.88–158.37 | ✅ | Resistance test / upthrust watch | At 52-week high ~$158.37, rejected Oct 19. Watch for upthrust (break above then reverse → avoid/short) or confirmed breakout with volume → long. |
| EQNR | 12.46 (financecharts 10-21) / 11.47 (macrotrends 10-20) / 12.6553 (companiesmarketcap) / 12.52 (public 10-19) / 12.3 (wallstsmart) | Energy | ~$46.11–46.17 | ✅ | Strong uptrend, not extended | Above SMA 50 & 200. RSI 69.7 (carryover). Wait for pullback to SMA 50 (~$43) for Spring/SOS entry. Not an entry here. |
| B (Barrick) | 10.51 (financecharts 10-21) / 13.8459 (companiesmarketcap) / 13.7 (investing.com) / 10.40 (public 10-19) | Materials | ~$40.43–40.76 | ✅ | Bearish (markdown/distrib) | Avoid longs. Strongly bearish MAs, RSI 46.59, MACD -0.64 (carryover). Wait for selling climax or Spring before considering. |
| PDD | 8.96 (macrotrends 10-19) / 8.52 (companiesmarketcap) / 9.05 (public 10-20) / 8.3 (vcpscanner 10-20) / 8.15 (fullratio 10-21) | Consumer Disc. | ~$78.72–81.39 | ✅ | Base building / Spring watch | Price below SMA 50/100/200 (carryover). RSI 55.01, MACD 0.25 bullish. P/E well above value-trap threshold of 5. Watch for confirmed Spring/SOS at support. (Note: financecharts shows 1.22 — data error; consensus ~8.5–9.05.) |
| CVE | 12.72 (financecharts 10-21) / 12.70 (public 10-20) / 12.2506 (companiesmarketcap) / 12.85 (wisesheets 10-21) | Energy | ~$32.00–33.13 | ✅ | Strong uptrend, pullback watch | Strongly bullish (17/26), above all MAs (carryover). RSI 59 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Ticker "B" ambiguity:** Searches for ticker "B" returned Barnes & Noble Education (BNED, P/E 18.19–1281 — fails) and BNY Mellon (BNY, P/E 15.55–16.64 — fails). The notes treat "B" as Barrick Gold (P/E ~10.4–13.8, passes). Barrick's actual NYSE ticker is GOLD, not B. Confirm the intended ticker before acting.

**Actionable setups (10-22):**
1. **PYPL — Spring/SOS played out:** Bounced Oct 20 at support cluster on heavy volume, now above 50 SMA at ~$57.14. RSI 58.5 (not overbought), MACD 0.53 bullish. Not an immediate entry — wait for pullback to ~$56 support for fresh SOS confirmation before entering long (€30K day trade bucket).
2. **EQNR — Watch pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Alert on retest of 50-day MA for Spring/SOS.
3. **CVE — Watch pullback to support:** Strongly bullish markup, not extended (RSI 59). Alert on first meaningful pullback for Spring/SOS.
4. **EOG — Watch resistance ~$158.37 (52-week high):** Rejected Oct 19. Upthrust = avoid/short; breakout with volume = long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring.
6. **PDD — Watch for Spring in base:** Only on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

**Next steps:**
- Set price alerts: PYPL pullback to ~$56; EQNR pullback to ~$43; CVE pullback to support; EOG breakout/upthrust at ~$158.37
- PYPL is the only near-term actionable setup (long on fresh SOS confirmation after pullback)
- Verify P/E on IBKR Fundamentals tab before executing (brokerage connection still stuck)
- Confirm ticker "B" identity before acting on Barrick data
- Refresh technical chart data next run to confirm/no-new Spring/SOS or Upthrust/SOW


**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus; PDD financecharts 1.22 is a known data error — consensus ~8.5–9.05). Fresh P/E pulled via web_search (financecharts, macrotrends, companiesmarketcap, public.com, fullratio, ycharts, wallstsmart, stockrow, coinglass). IBKR brokerage connection still stuck — P/E not yet verified on IBKR Fundamentals tab. US market not yet open (10:47 UTC ≈ 6:47 AM ET); no fresh intraday/volume feed. PYPL technical picture updated from web sources (financhill Oct 18, tickzen Oct 20, wallstsmart).

| Stock | P/E (fresh, 10-22) | Sector | Price | P/E Pass <15 | Wyckoff Signal | Action |
|---|---|---|---|---|---|---|
| PYPL | 10.79 (financecharts 10-21) / 10.80 (public 10-20) / 10.7 (companiesmarketcap) / 10.73 (fullratio 10-21) / 10.81 (ycharts 10-21) / 10.6× (stockrow 10-16) | Financials | ~$56.51–57.20 | ✅ | **Spring/SOS played out** — bounced Oct 20 at support cluster on heavy volume, now above 50 SMA ($56.03). RSI 58.5, MACD 0.53 bullish. | Not an immediate entry at current price — wait for pullback to support (~$56) for fresh SOS confirmation. Day trade candidate (€30K bucket). |
| DHI | 13.21 (financecharts 10-21) / 13.04 (macrotrends 10-1) / 13.2 (stockrow 10-16) / 13.34 (public 10-20) | Consumer Disc. | ~$136.13 | ✅ | No clear signal | Watchlist only — volume quiet (0.71x avg). Hold off until volume confirms. |
| EOG | 12.29 (financecharts 10-21) / 12.26 (public 10-19) / 11.2× (stockrow 10-6) | Energy | ~$157.88–158.37 | ✅ | Resistance test / upthrust watch | At 52-week high ~$158.37, rejected Oct 19. Watch for upthrust (break above then reverse → avoid/short) or confirmed breakout with volume → long. |
| EQNR | 12.46 (financecharts 10-21) / 11.47 (macrotrends 10-20) / 12.6553 (companiesmarketcap) / 12.52 (public 10-19) / 12.3 (wallstsmart) | Energy | ~$46.11–46.17 | ✅ | Strong uptrend, not extended | Above SMA 50 & 200. RSI 69.7 (carryover). Wait for pullback to SMA 50 (~$43) for Spring/SOS entry. Not an entry here. |
| B (Barrick) | 10.51 (financecharts 10-21) / 13.8459 (companiesmarketcap) / 13.7 (investing.com) / 10.40 (public 10-19) | Materials | ~$40.43–40.76 | ✅ | Bearish (markdown/distrib) | Avoid longs. Strongly bearish MAs, RSI 46.59, MACD -0.64 (carryover). Wait for selling climax or Spring before considering. |
| PDD | 8.96 (macrotrends 10-19) / 8.52 (companiesmarketcap) / 9.05 (public 10-20) / 8.3 (vcpscanner 10-20) / 8.15 (fullratio 10-21) | Consumer Disc. | ~$78.72–81.39 | ✅ | Base building / Spring watch | Price below SMA 50/100/200 (carryover). RSI 55.01, MACD 0.25 bullish. P/E well above value-trap threshold of 5. Watch for confirmed Spring/SOS at support. (Note: financecharts shows 1.22 — data error; consensus ~8.5–9.05.) |
| CVE | 12.72 (financecharts 10-21) / 12.70 (public 10-20) / 12.2506 (companiesmarketcap) / 12.85 (wisesheets 10-21) | Energy | ~$32.00–33.13 | ✅ | Strong uptrend, pullback watch | Strongly bullish (17/26), above all MAs (carryover). RSI 59 neutral, MACD 0.31 bullish. Wait for pullback to support for Spring/SOS entry. |

**Actionable setups (10-22):**
1. **PYPL — Spring/SOS played out:** Bounced Oct 20 at support cluster on heavy volume, now above 50 SMA at ~$56.51–57.20. RSI 58.5 (not overbought), MACD 0.53 bullish. Not an immediate entry — wait for pullback to ~$56 support for fresh SOS confirmation before entering long (€30K day trade bucket).
2. **EQNR — Watch pullback to SMA 50 (~$43):** Not an entry at RSI 69.7. Alert on retest of 50-day MA for Spring/SOS.
3. **CVE — Watch pullback to support:** Strongly bullish markup, not extended (RSI 59). Alert on first meaningful pullback for Spring/SOS.
4. **EOG — Watch resistance ~$158.37 (52-week high):** Rejected Oct 19. Upthrust = avoid/short; breakout with volume = long.
5. **B — Avoid longs:** Bearish distribution/markdown. Wait for selling climax or Spring.
6. **PDD — Watch for Spring in base:** Only on confirmed Spring/SOS.
7. **DHI — No action:** Volume too quiet to confirm SOS.

**Next steps:**
- Set price alerts: PYPL pullback to ~$56; EQNR pullback to ~$43; CVE pullback to support; EOG breakout/upthrust at ~$158.37
- PYPL is the only near-term actionable setup (long on fresh SOS confirmation after pullback)
- Verify P/E on IBKR Fundamentals tab before executing (brokerage connection still stuck)
- Refresh technical chart data next run to confirm/no-new Spring/SOS or Upthrust/SOW

### Account Status (2026-10-21)
- IBKR Paper Account U23339441 — LOGGED IN ✅
- NAV: €1,011,277.55 EUR
- Cash: €1,005,130.60 EUR
- Available Funds: €1,010,189.53 EUR
- Buying Power: €6,734,596.86 EUR
- Allocation: €30K day trades + €30K swing holds
- Brokerage connection: STUCK — Log in button clicked, progress bar spins but never completes. Tried multiple times over 10+ minutes.

### Trading Plan
- Market: US stocks only
- Filter: Relatively low P/E
- Method: Wyckoff accumulation/distribution analysis
- Timeframe: 30 days
- Styles: Day trades + Swing holds

### Blocker
- IBKR Market Screener brokerage connection stuck in "connecting" state. Web portal may not support paper trading connections reliably. Fallback: IBKR Desktop/TWS app or manual mobile trading.

### Non-Tech Value Screener Sources
- Chartmill Low P/E screener: https://www.chartmill.com/stock/markets/usa/screener/low-pe-stocks
- TipRanks lowest P/E: https://www.tipranks.com/compare-stocks/lowest-pe-stocks
- Elite Stock Research low P/E: https://www.elitestockresearch.com/lists/low-pe-value-stocks

### Candidate Stocks — Low P/E US Watchlist (in progress)

**Screening criteria:**
- US market (NASDAQ/NYSE)
- P/E ratio < 15 (or below sector median)
- Adequate liquidity for day trades (avg volume > 500K)
- Wyckoff-compatible: building accumulation ranges or showing SOS patterns

**Checked (Tech Giants — rejected):**
- AAPL — P/E 39.07 — ❌ TOO HIGH
- MSFT — P/E 29.64 — ❌ TOO HIGH

**✅ Non-Tech Low P/E Candidates (P/E refreshed 10/21/2026):**
- PDD — P/E 8.52–8.98, Consumer Discretionary, NASDAQ (Chinese ADR), FA Rating 7/10
- EQNR — P/E 11.57–12.48, Energy, NYSE, FA Rating 6/10
- EOG — P/E 11.2–12.30, Energy, NYSE, FA Rating 6/10
- B — P/E 10.40–13.8, Materials, NYSE, FA Rating 7/10
- CVE — P/E 12.25–12.85, Energy, NYSE (Canadian), FA Rating 6/10
- PYPL — P/E 10.78, Financials, NASDAQ, FA Rating 6/10
- DHI — P/E 13.04–13.25, Consumer Discretionary, NYSE, FA Rating 6/10

**Day trades (€30K):**
- PYPL — P/E 10.78, Financials
- DHI — P/E 13.04–13.25, Consumer Discretionary (watchlist only until volume confirms)

**Swing holds (€30K):**
- EQNR — P/E 11.57–12.48, Energy — integrated oil major
- EOG — P/E 11.2–12.30, Energy — pure-play E&P
- B — P/E 10.40–13.8, Materials — gold miner
- PDD — P/E 8.52–8.98, Consumer Discretionary
- CVE — P/E 12.25–12.85, Energy — Canadian oil sands

**Next:**
1. Apply Wyckoff analysis to each candidate (accumulation ranges, Springs, SOS)
2. Verify P/E on IBKR fundamentals
3. Execute paper trades on best setups

---

## Trade Cycle Log (Alpaca + YFinance + IBKR TWS)

### 2026-10-22 15:12:57 — Full Cycle Complete
- **Account:** NAV €1,011,171.17, Cash €1,005,058.72
- **Alpaca Quotes:** All 7 stocks retrieved successfully
- **YFinance Bars:** All 7 stocks — 30 daily bars each
- **IBKR TWS:** Connected on port 7497
- **Wyckoff Signals:** All NEUTRAL — no clear Springs/SOS or Upthrust/SOW patterns
- **Trades Placed:** None (correct Wyckoff discipline — don't trade without confirmed setup)

**Current Quotes:**
- PYPL: 54.15/60.13 | DHI: 132.28/149.63 | EQNR: 46.59/46.66 | EOG: 148.16/169.51 | B: 35.08/— | PDD: 67.54/90.42 | CVE: 28.38/—

### Findings & Optimization Notes
- Wyckoff signal detection may be too strict — consider adding RSI, volume divergence, intraday timeframe analysis
- RSS news feed for these tickers would help confirm fundamental catalysts
- Paper account has €1M+ available — ready to deploy €40K allocation when signals trigger
- Blackout authorized: update scripts, buy/sell, optimize as needed
### Wyckoff Check Results — 2026-10-22 (cron run #9, 14:17 UTC / 17:17 MSK)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus; PDD financecharts 1.22 is a known data error — consensus ~8.5–9.05). IBKR brokerage connection still stuck — P/E not verified on IBKR Fundamentals tab. No fresh intraday/volume feed this run; Wyckoff technical signals carry over from 10-21 and the 15:12:57 full cycle (all NEUTRAL). US market open (~10:17 AM EDT).

| Stock | P/E (consensus) | Wyckoff Signal (carryover) | Action |
|---|---|---|---|
| PYPL | ~10.7–10.8 | Spring/SOS played out (Oct 20) | Wait for pullback to ~$56 for fresh SOS before entering long (€30K day trade) |
| DHI | ~13.0–13.3 | No clear signal | Watchlist only — volume quiet (0.71x avg) |
| EOG | ~12.3 | Resistance test / upthrust watch | Watch ~$158.37: upthrust = avoid/short; breakout w/ volume = long |
| EQNR | ~12.4–12.5 | Strong uptrend, not extended | Wait for pullback to SMA 50 (~$43) for Spring/SOS entry |
| B | ~10.4–13.8 | Bearish (markdown/distrib) | Avoid longs; wait for selling climax or Spring |
| PDD | ~8.5–9.0 | Base building / Spring watch | Only on confirmed Spring/SOS at support |
| CVE | ~12.3–12.9 | Strong uptrend, pullback watch | Wait for pullback to support for Spring/SOS entry |

**Actionable setups:** None new this run. PYPL remains the only near-term actionable setup, pending pullback to ~$56 for fresh SOS confirmation. All other names are watches/avoids. No Upthrust/SOW sell signals confirmed; EOG resistance test is the closest watch.

**Blocker:** IBKR brokerage connection stuck; no fresh price/volume feed. Wyckoff signals cannot be newly confirmed.

## Wyckoff Check Results — 2026-10-22 (cron run #10, 14:47 UTC / 17:47 MSK)

**All 7 watchlist stocks pass P/E < 15 filter.** No value-trap flags (none below P/E 5 on consensus; PDD financecharts 1.22 is a known data error — consensus ~8.5–9.05). IBKR brokerage connection still stuck — P/E not verified on IBKR Fundamentals tab. No fresh intraday/volume feed this run; Wyckoff technical signals carry over from 10-21 and the 15:12:57 full cycle (all NEUTRAL). US market open (~10:47 AM EDT).

| Stock | P/E (consensus) | Wyckoff Signal (carryover) | Action |
|---|---|---|---|
| PYPL | ~10.7–10.8 | Spring/SOS played out (Oct 20) | Wait for pullback to ~$56 for fresh SOS before entering long (€30K day trade) |
| DHI | ~13.0–13.3 | No clear signal | Watchlist only — volume quiet (0.71x avg) |
| EOG | ~12.3 | Resistance test / upthrust watch | Watch ~$158.37: upthrust = avoid/short; breakout w/ volume = long |
| EQNR | ~12.4–12.5 | Strong uptrend, not extended | Wait for pullback to SMA 50 (~$43) for Spring/SOS entry |
| B | ~10.4–13.8 | Bearish (markdown/distrib) | Avoid longs; wait for selling climax or Spring |
| PDD | ~8.5–9.0 | Base building / Spring watch | Only on confirmed Spring/SOS at support |
| CVE | ~12.3–12.9 | Strong uptrend, pullback watch | Wait for pullback to support for Spring/SOS entry |

**Actionable setups:** None new this run. PYPL remains the only near-term actionable setup, pending pullback to ~$56 for fresh SOS confirmation. All other names are watches/avoids. No Upthrust/SOW sell signals confirmed; EOG resistance test remains the closest watch. Wyckoff signal detection unchanged (all NEUTRAL from 15:12 full cycle).

**Blocker:** IBKR brokerage connection stuck; no fresh price/volume feed. Wyckoff signals cannot be newly confirmed.

## Wyckoff Check Results — 2026-10-22 (cron run #11, 18:17 UTC / 21:17 MSK) — LIVE DATA

**First run with working price/volume feed.** Yahoo chart API (1d / 5m / 15m) returned live data for all 7 names; 18:17 UTC = ~2h47m into the US session, ~1h43m to close. Volume figures are time-adjusted pace vs 20d avg, not raw comparison.

P/E could not be re-pulled fresh this run (Yahoo quoteSummary returned 401). Consensus values from run #10 still stand; all 7 remain below the 15 threshold.

| Stock | Price (18:17 UTC) | Chg | Vol pace | RSI14 | SMA20 | SMA50 | Wyckoff Read | Action |
|---|---|---|---|---|---|---|---|---|
| PYPL | $57.12 | -0.13% | 0.69x | 86.6 | 55.31 | 55.92 | Top of range ($57.95), no supply/demand signal, overbought | **No entry.** Wait for pullback to ~$56 for fresh SOS. RSI 86.6 = do not chase. |
| DHI | $146.51 | **+5.42%** | 1.24x | 64.6 | 137.31 | 141.09 | **SOS — jump across the creek.** Broke 20d range high $142.90 on a wide bar, closed near high ($147.25 day high, $146.51 close) | **Actionable long — but not at market.** Wait for LPS/backup to $143–144. Earnings 10-29 = event risk inside swing horizon. |
| EQNR | $46.31 | +0.46% | 1.67x | 68.5 | 43.78 | 43.27 | Effort without result at 52w high $47.01 — opened $46.76, high $46.99, closed $46.31 (lower half) on elevated volume. **Minor upthrust** | **Stand aside.** Do not add at highs. Prior plan (pullback to SMA50 ~$43) still valid. |
| EOG | $157.82 | ~flat | 0.83x | 88.8 | 148.51 | 147.13 | **Upthrust confirmed intraday** — broke to new 52w high $160.31, reversed to close $157.82, below prior close $157.88. Volume light (0.83x) = weak effort, so not a high-conviction short | **Avoid longs / no short.** Failed breakout at resistance. Reassess only on reclaim of $160.31 with volume. |
| B (Barrick) | $38.44 | **-5.67%** | 1.74x | 42.3 | 40.44 | 42.73 | **SOW** — wide down bar, closed $0.10 off day low, at bottom of 20d range ($38.36), 1.74x volume. Below all MAs | **Avoid / no long.** Markdown in progress. Wait for selling climax + Spring. |
| PDD | $79.38 | +0.84% | 1.68x | 63.3 | 79.33 | 81.34 | Range-bound $74.72–83.88, straddling SMA20, below SMA50. No edge | **No action.** Needs Spring at $74–75 or SOS over $83.88. |
| CVE | $32.38 | -2.25% | 1.49x | 49.9 | 31.92 | 32.14 | Down bar from range top $33.79, sold to $31.85 then recovered above SMA20/50. Possible shakeout, unconfirmed | **Watch.** Confirmation = close back over $33.79 on volume. Invalidation = close below $31.85. |

**Actionable setups (10-22, live):**
1. **DHI — Long (SOS breakout), entry on LPS only.** Breakout from $130.40–142.90 range on 1.24x pace, close near high, RSI 64.6 (not overbought). Buy zone $143–144.50 on a low-volume backup; stop below $138.70 (today's low / range mid); first target measured move $155.5 (range width $12.50 added to $143). Sizing €30K day/short-swing bucket. **Caveat: Q4 earnings Thu 10-29 — either exit before the print or halve size.**
2. **B — Sell/avoid signal.** 1.74x down bar closing at range low. No short recommended (paper account, no borrow check done); simply do not initiate longs.
3. **EOG — Upthrust warning.** New 52w high then reversal close. Do not buy the breakout.
4. **EQNR — Effort vs result divergence at highs.** Stand aside.
5. **PYPL — Overbought at range top.** No entry; the Oct 20 Spring/SOS has played out.
6. **PDD, CVE — Neutral.** No confirmation either way.

**Trades placed:** None. DHI is the only valid setup and it is a chase at $146.51, +5.4% off the prior close with earnings in five sessions. Correct Wyckoff entry is the backup, not the breakout bar.

**Note:** Signals flipped materially vs. the carryover readings in runs #4–#10. The carryover "all NEUTRAL" was an artifact of having no live feed, not a market condition. Future runs must use the live feed.

## Wyckoff Check Results — 2026-10-22 (cron run #12, 18:47 UTC / 21:47 MSK) — LIVE

Live Yahoo feed (6mo/1d + 2d/5m). ~1h13m left in the US session. P/E refresh failed again (Yahoo quoteSummary 401) — run #10 consensus values stand, all 7 < 15.

| Stock | Price | Day % | Close-pos in range | Vol pace | RSI14 | Wyckoff Read | Action |
|---|---|---|---|---|---|---|---|
| PYPL | $57.08 | -0.2% | 34% | 0.62x | 86.1 | Fading from $57.61 high, overbought at range top | No entry; wait pullback ~$56 |
| DHI | $146.49 | +5.4% | 91% | 1.49x | 64.5 | **SOS confirmed** — held all day above VWAP 144.93, closed near high, sector-wide (ITB +4.6%, XHB +2.9%) | Long only on LPS backup $143–144.5; not at market |
| EQNR | $46.44 | +0.7% | 68% | 1.09x | 68.9 | Recovered off $45.26, stalling under 52w high $47.01 | Stand aside |
| EOG | $158.09 | +0.1% | 59% | 0.82x | 88.9 | Upthrust intact: 160.31 high rejected, light volume | Avoid longs |
| B | $38.37 | -5.9% | 5% | 1.55x | 42.0 | **SOW confirmed at close** — new 20d low 38.31, wide bar, closes on low | Avoid / no long |
| PDD | $79.04 | +0.4% | 67% | 0.84x | 62.4 | Range $74.72–83.88, no edge | No action |
| CVE | $32.38 | -2.3% | 31% | 1.31x | 49.9 | Dipped 31.85, closed lower half; shakeout unconfirmed | Watch; confirm > 33.79 |

**Actionable:** DHI long setup still valid but entry is the LPS backup ($143–144.50, stop < $138.70, target $155.5). Earnings 10-29 = halve size or exit before print.
**Trades placed:** None — DHI is the only setup and it is a breakout chase at $146.49; weekly TF has not broken its 20-week high ($170.79), so it fails the 2-timeframe agreement rule.

## Wyckoff Check Results — 2026-10-23 (cron run #13, 07:17 UTC / 10:17 MSK) — PRE-MARKET, LIVE DATA

**This run fixed two silent execution bugs that had been masking results (see "Script fixes" below).**

Pre-market: 07:17 UTC = 03:17 EDT, ~6h to the US open. Bars are the settled 10-22 daily close; the
1d bar does carry the live in-progress bar once the session starts, so these are pre-open snapshots.

P/E refreshed via yfinance `.info` (brokerage connection is now up — see below — but P/E was read from
consensus instead). **All 7 pass the P/E < 15 filter.** No value-trap flags (nothing below 5; PDD 8.91
is the lowest and is a genuine multiple, not the 1.22 data error previously noted).

| Stock | P/E | Price (10-22 close) | Day % | 20d range pos | RSI14 D/W/M | Vol x | Wyckoff Read | Action |
|---|---|---|---|---|---|---|---|---|
| PYPL | 10.75 | $57.53 | +0.59% | 93% | 88.3 / 52.0 / 40.7 | 0.68x | Overbought at range top ($57.95), no supply signal; Oct-20 Spring/SOS played out | **No entry.** Earnings **Oct 27** (4 days). Wait pullback ~$56. |
| DHI | 14.08 | $147.66 | **+6.25%** | **99.6%** | 65.6 / 48.7 / 44.0 | 1.04x | **SOS / jump across the creek (DAILY)** — new 20d high $147.73, wide bar, close 99% of bar range. Weekly still under its 20w high $170.28 (43% of w-range), monthly 53% of m-range | **Daily-only SOS → fails 2-TF rule.** Correct entry is the LPS backup $143–144.50; stop < $138.70; target $155.5. Earnings **Oct 29**. Homebuilders ripped sector-wide: ITB +5.39%, XHB +3.77%. |
| EQNR | 12.68 | $46.42 | +0.65% | 90% | 68.8 / 70.4 / 73.7 | 1.02x | Extended at highs — 96% of weekly range, 98% of monthly, 52w high $47.01 immediate overhead. Effort w/o result, but today's volume 1.02x does **not** confirm an upthrust | **Stand aside.** Entering at the highs is the worst Wyckoff entry. |
| EOG | 12.28 | $157.96 | +0.05% | 90% | 89.4 / 61.9 / 65.0 | 0.79x | **Upthrust unresolved** — 160.31 high rejected, today closes mid-bar (56%) on light 0.79x volume. Weak effort = no short conviction either | **Avoid longs.** Reassess only on a close over $160.31 with volume. Earnings Nov 5. |
| B | 9.99 | $38.65 | **-5.18%** | 8.7% | 43.0 / 56.9 / 60.6 | 1.25x | **SOW / markdown continuing** — new 20d low $38.24, closes in lower third, below SMA20/50/200. Sector-wide: GDX -5.80%, GLD -2.63% | **Avoid / no long.** Wait for selling climax + Spring. Earnings Nov 9. |
| PDD | 8.91 | $79.17 | +0.57% | 49% | 62.7 / 44.4 / **30.0** | 1.08x | Base-building at the bottom of the 2y range (11% of range, -43% from $139.41). Range $74.72–83.88, straddling SMA20, under SMA50 | **Watch.** Spring at $74–75 → long. SOS over $83.88 → long. Nothing yet. Earnings Nov 18. |
| CVE | 12.75 | $32.01 | -3.38% | 45% | 47.4 / 61.2 / 78.0 | 1.12x | Down bar from range top $33.79, **closed 9% of bar range** (on the low) — supply present, but mid-20d-range so no SOW label | **Watch.** Confirmation = close over $33.79 on volume. Invalidation = close below $30.54. Earnings Oct 29. |

**Actionable setups this run:** only **DHI** — a clean daily SOS. It is deliberately **not traded**: it is
1 of 3 timeframes, and the skill's rule is 2+ agreement before risking the €30K bucket. Add earnings on
Oct 29 for a swing horizon that reaches the print, and the disciplined answer stays "no trade."

**Trades placed: none.** Now a *verified* decision, not a silent failure — the order path was proven
end-to-end this run with a non-marketable resting order that was submitted and then cancelled cleanly.

**Context:** QQQ -2.86%, SPY -1.18% on 10-22, but homebuilders (ITB +5.39%) and regional banks
(KRE +2.53%) rallied hard while gold miners (GDX -5.80%) broke down. DHI's move is a rate-sensitive
sector move, not company-specific; B's decline is a gold-complex move. Both matter for entry timing.

### Script fixes (2026-10-23) — /tmp/wyckoff_v4.py

1. **Order sizing bug (critical).** The €30K bucket was being passed as `totalQuantity`, i.e. an order
   for **30,000 SHARES** (~$4.4M notional per name, ~$100M across the watchlist) on a ~€1.01M paper
   account. Now: `place_market_order(app, symbol, notional, action, price)` computes
   `quantity = int(notional // price)` and refuses to send if notional < 1 share. Also switched MKT → LMT
   (0.5% through the reference) so a bad reference cannot market-fill at a nonsense price.
2. **`eTradeOnly` rejection (critical).** `ibapi` 9.81.1 defaults `Order.eTradeOnly = True`; TWS paper
   rejects any order carrying it with **error 10268 "The 'EtradeOnly' order attribute is not supported"**
   — the order never reached `orderStatus`/`openOrder` at all. Silent no-op on every attempted trade.
   Fixed by setting `eTradeOnly = False`, `firmQuoteOnly = False`, `tif = "DAY"` explicitly.
   Proven: BUY 600 DHI @ LMT 50.25 → `PreSubmitted` → cancel → `Cancelled`.
3. **Signal price corruption.** `wyckoff_signal_for_timeframe` used the Alpaca quote as `current_price`.
   The free-tier/IEX quote is stale and wide (B: bid 33.06 vs close 38.65 — a 15% error; PYPL bid 53.92
   vs close 57.53), which flipped every pattern test to NEUTRAL regardless of the market. Now the
   reference price is the latest bar close; the quote is only used as a fallback and is rejected when it
   disagrees with the bar close by >20%.
4. **Spurious trade filter.** The cycle queued a BUY on *any* LONG, including single-timeframe signals,
   contradicting the skill's 2-TF rule. Now gated on `reason.startswith("Multi-TF")`.
5. **Log noise.** ibapi's client/wrapper loggers dumped every REQUEST/SENDING/ANSWER frame at INFO,
   burying the analysis. Set to WARNING.

**IBKR connection status: RESOLVED.** Port 7497 is listening (TWS Classic pid 8682), `startApi`
succeeds, account summary returns **NAV €1,011,033.99, Cash €1,005,051.07** (paper DUO957759). The
earlier "brokerage connection stuck" blocker in runs #9–#12 was the harness, not TWS. Positions: only
`XAGUSD 101 @ 80.01` (pre-existing, unrelated to this strategy).

**Caveat on the bucket sizes:** the €30K figures are EUR, the account base is EUR, but US stock orders
are in USD. No FX conversion is applied — 30,000 units are spent as USD. Flag for the user before this
is treated as real sizing discipline.

### Run log — 2026-10-23 11:17 MSK (automation wyckoff-30min-check)

Data unchanged from the 10:28 run (US market closed — 08:17 UTC / 04:17 ET pre-market; yfinance still
returns the Oct-22 settled bars). Deterministic multi-TF scan over the 22-name watchlist:
**0 LONG, 0 SHORT, 22 NEUTRAL — no actionable setups, no trades queued.**

Close-up on the 7 requested names (same numbers as 10:28, no new bar):
- PYPL $57.53 — 93% of 20d range, 0.68x vol → overbought, no supply; earnings Oct 27.
- DHI $147.66 — new 20d high, wide bar, close 99% of range, but vol only 1.06x (rule needs >1.5x) →
  NEUTRAL; prior note's daily label was qualitative only. Wait for LPS backup $143–144.50.
- EQNR $46.42 — 90/96/98% of D/W/M range, extended at highs, 1.02x vol → stand aside.
- EOG $157.96 — $160.31 high rejected, mid-bar close, 0.79x vol → no resolution either way.
- B $38.65 — 8.7% of 20d range, 1.25x vol, lower-third close → SOW/markdown continues; avoid longs.
- PDD $79.17 — 49% of 20d range, 10.7% of 2y range, RSI(m) 30 → base-building; watch $74–75 spring.
- CVE $32.01 — down bar closing 9% of range from $33.79 top, 1.12x vol → supply, but mid-range, not SOW.

Engine health: TWS Classic port 7497 listening, startApi OK, paper account NAV €1,011,042.93 /
Cash €1,005,055.96. Order path previously proven (non-marketable LMT → PreSubmitted → Cancelled).

### Wyckoff Check Results — 2026-10-23 (cron run #14, 10:47 UTC / 13:47 MSK) — PRE-MARKET

US market closed (opens 13:30 UTC / 16:30 MSK). No new live bars since run #13 (07:17 UTC); yfinance returns the Oct-22 settled closes. Deterministic multi-TF scan unchanged: **0 LONG, 0 SHORT, 22 NEUTRAL — no actionable setups, no trades queued.**

| Stock | P/E | Price (10-22 close) | Wyckoff Read | Action |
|---|---|---|---|---|
| PYPL | 10.75 | $57.53 | Overbought at range top, Oct-20 Spring/SOS played out | No entry. Earnings Oct 27. Wait pullback ~$56. |
| DHI | 14.08 | $147.66 | Daily-only SOS (99.6% of 20d range) — fails 2-TF rule | Wait for LPS backup $143–144.50. Earnings Oct 29. |
| EQNR | 12.68 | $46.42 | Extended at highs (90/96/98% of D/W/M range) | Stand aside. |
| EOG | 12.28 | $157.96 | Upthrust unresolved (160.31 high rejected, 0.79x vol) | Avoid longs. |
| B | 9.99 | $38.65 | SOW/markdown continues (8.7% of 20d range, 1.25x vol) | Avoid / no long. |
| PDD | 8.91 | $79.17 | Base-building (10.7% of 2y range, RSI m 30) | Watch $74–75 spring. |
| CVE | 12.75 | $32.01 | Down bar from range top, supply present, mid-range | Watch >$33.79 / <$30.54. |

**Trades placed:** None. IBKR TWS paper (port 7497) connected, NAV €1,011,042.93 / Cash €1,005,055.96. Order path proven end-to-end (non-marketable LMT → PreSubmitted → Cancelled). No multi-TF confirmation on any name → no entry per skill's 2-TF rule.

**Next:** Re-run after US open (13:30 UTC) for fresh live bars/volume.
