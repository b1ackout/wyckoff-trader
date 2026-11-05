#!/usr/bin/env python3
"""Read-only paper executions and completed daily OHLCV into a private SQLite DB."""
import argparse
import logging
import math
import os
import sqlite3
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import trade_cycle as trader
from scan_watchlist import download_batch
from ibapi.execution import ExecutionFilter

ACCOUNT = 'DUO957759'
ET = ZoneInfo('America/New_York')
DB = Path.home() / '.openclaw/state/wyckoff-research/research.sqlite3'


def connect(path=DB):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    db = sqlite3.connect(path, timeout=20)
    os.chmod(path, 0o600)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS executions (
        account TEXT NOT NULL, exec_id TEXT NOT NULL, symbol TEXT NOT NULL,
        security_type TEXT NOT NULL, currency TEXT NOT NULL, side TEXT NOT NULL,
        shares REAL NOT NULL, price REAL NOT NULL, executed_at TEXT NOT NULL,
        order_id INTEGER NOT NULL, perm_id INTEGER NOT NULL, order_ref TEXT NOT NULL,
        exchange TEXT NOT NULL, collected_at TEXT NOT NULL,
        PRIMARY KEY (account, exec_id));
      CREATE TABLE IF NOT EXISTS daily_bars (
        symbol TEXT NOT NULL, session_date TEXT NOT NULL, source TEXT NOT NULL,
        currency TEXT NOT NULL, open REAL NOT NULL, high REAL NOT NULL,
        low REAL NOT NULL, close REAL NOT NULL, volume INTEGER NOT NULL,
        collected_at TEXT NOT NULL, PRIMARY KEY (symbol, session_date, source));
    ''')
    return db


def save_executions(db, rows, collected_at):
    with db:
        for r in rows:
            if r['account'] != ACCOUNT or not all(math.isfinite(float(r[k])) and float(r[k]) > 0 for k in ('shares', 'price')):
                raise ValueError('invalid paper execution')
            db.execute('''INSERT OR IGNORE INTO executions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (r['account'], r['exec_id'], r['symbol'], r['security_type'], r['currency'],
                        r['side'], r['shares'], r['price'], r['executed_at'], r['order_id'],
                        r['perm_id'], r['order_ref'], r['exchange'], collected_at))
    return db.execute('SELECT count(*) FROM executions').fetchone()[0]


def save_bars(db, bars, collected_at, today=None):
    today = today or datetime.now(ET).date().isoformat()
    inserted = 0
    with db:
        for symbol, series in bars.items():
            for b in series:
                day = str(b['t'])[:10]
                if day >= today:  # today's bar is unfinished; never label it official close/high/low
                    continue
                o,h,l,c = (float(b[k]) for k in ('o','h','l','c'))
                v = int(b['v'])
                if not (all(math.isfinite(x) and x > 0 for x in (o,h,l,c)) and l <= min(o,c) <= max(o,c) <= h and v >= 0):
                    continue
                cur = db.execute('''INSERT OR IGNORE INTO daily_bars VALUES (?,?,?,?,?,?,?,?,?,?)''',
                                 (symbol, day, 'yfinance', 'USD', o,h,l,c,v,collected_at))
                inserted += cur.rowcount
    return inserted


def broker_executions():
    log = logging.getLogger(); previous = log.level; log.setLevel(logging.WARNING)
    app = trader.IBKRApp(); accounts = []; rows = []
    account_ready = threading.Event(); finished = threading.Event(); errors = []
    app.managedAccounts = lambda ids: (accounts.extend(ids.split(',')), account_ready.set())
    app.execDetails = lambda req, contract, ex: rows.append(dict(
        account=ex.acctNumber, exec_id=ex.execId, symbol=contract.symbol,
        security_type=contract.secType, currency=contract.currency, side=ex.side,
        shares=float(ex.shares), price=float(ex.price), executed_at=str(ex.time),
        order_id=int(ex.orderId), perm_id=int(ex.permId), order_ref=ex.orderRef or '',
        exchange=ex.exchange or '')) if req == 191 else None
    app.execDetailsEnd = lambda req: finished.set() if req == 191 else None
    old_error = app.error
    def on_error(req, code, message, *args):
        old_error(req, code, message, *args)
        if code not in (2104, 2106, 2158, 2186): errors.append((code, message))
    app.error = on_error
    try:
        app.connect('127.0.0.1', 7497, clientId=191)
        threading.Thread(target=app.run, daemon=True).start()
        if not account_ready.wait(8) or accounts != [ACCOUNT]:
            raise RuntimeError('paper account identity unavailable')
        filt = ExecutionFilter(); filt.acctCode = ACCOUNT
        app.reqExecutions(191, filt)
        if not finished.wait(20) or errors:
            raise RuntimeError('broker execution response incomplete or errored: ' + str(errors[-1:] ))
        return rows
    finally:
        try: app.disconnect()
        finally: log.setLevel(previous)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bars-only', action='store_true')
    parser.add_argument('--fills-only', action='store_true')
    parser.add_argument('--db', type=Path, default=DB)
    args = parser.parse_args()
    if args.bars_only and args.fills_only: parser.error('select one source or neither')
    collected = datetime.now(timezone.utc).isoformat()
    with connect(args.db) as db:
        if not args.bars_only:
            rows = broker_executions()
            print('Broker executions returned', len(rows), 'stored total', save_executions(db, rows, collected))
        if not args.fills_only:
            symbols = list(trader.WATCHLIST)
            bars = download_batch(symbols, '3mo', '1d')
            if not any(bars.values()): raise RuntimeError('no daily bars downloaded')
            print('Completed daily bars inserted', save_bars(db, bars, collected), 'symbols with data', sum(bool(bars[s]) for s in symbols), '/', len(symbols))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
