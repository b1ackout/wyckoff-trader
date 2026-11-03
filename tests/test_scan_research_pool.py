import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import scan_research_pool as r

class ResearchScanTests(unittest.TestCase):
    def test_canonical_is_forty_and_scan_matches(self):
        self.assertEqual(len(r.trader.WATCHLIST),40)
        self.assertEqual(len(r.universe()),40)
        self.assertEqual(set(r.CANDIDATES),set(r.trader.WATCHLIST))
        day=set(r.trader.DAY_TRADE_STOCKS)
        swing=set(r.trader.SWING_TRADE_STOCKS)
        self.assertEqual(len(day|swing),40)
        self.assertEqual(day & swing,set())
        self.assertEqual(day|swing,set(r.trader.WATCHLIST))
    def test_incomplete_quotes_block_report(self):
        bars=[{'c':100}]*25
        with patch.object(r,'download_batch',return_value={s:bars for s in r.universe()}),patch.object(r,'fetch_quotes',return_value=({},None)),contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(r.run(),2)
        self.assertIn('RESEARCH_DATA_INCOMPLETE',out.getvalue())
    def test_success_is_explicitly_read_only(self):
        bars=[{'c':100}]*25
        quotes={s:{'bid':99,'ask':100} for s in r.universe()}
        with patch.object(r,'download_batch',return_value={s:bars for s in r.universe()}),patch.object(r,'fetch_quotes',return_value=(quotes,None)),patch.object(r,'quote_quality',return_value=(.01,'OK')),patch.object(r.trader,'analyze_wyckoff_multitf',return_value=('LONG','',{'daily':'LONG','weekly':'NEUTRAL','monthly':'NEUTRAL'})),contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(r.run(),0)
        self.assertIn('no orders placed',out.getvalue())

if __name__=='__main__':unittest.main()
