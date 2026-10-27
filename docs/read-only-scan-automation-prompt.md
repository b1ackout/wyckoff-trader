Read-only Wyckoff signal scan for the canonical watchlist.

Run exactly one command with no arguments: `/home/deck/.openclaw/state/venvs/wyckoff/bin/python3 /home/deck/.openclaw/workspace/wyckoff-trader/scripts/scan_watchlist.py`. The script loads the canonical WATCHLIST, downloads all symbols in three batched Yahoo Finance requests, and fetches all Alpaca quotes in one bulk request. Do not loop over symbols or make individual fetch_all_timeframes calls; that sequential path timed out at 30 names.

Return the script output as the report; it includes verified LONG/SHORT signals, timeframe consensus, latest daily closes, quote quality, and data gaps. Do not claim P/E was reverified. Stale, missing, zero, or wide quotes are not execution references. This is read-only: never invoke a trade cycle or place, modify, or cancel orders. Let configured automation delivery post the final report; do not call the message tool.
