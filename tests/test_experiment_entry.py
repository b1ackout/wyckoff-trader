import sys
import tempfile
import json
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import experiment_entry as e

class FakeApp:
    def disconnect(self): pass

class EntryTests(unittest.TestCase):
    def test_duplicate_position_skips_before_fetch(self):
        held={(e.ACCOUNT,"UBER"):(35,65.48,"STK","USD")}
        with patch.object(e,"market_open",return_value=True),patch.object(e,"broker_snapshot",return_value=(FakeApp(),held,{})),patch.object(e,"candidate") as candidate:
            self.assertEqual(e.run("UBER",execute=True),0)
            candidate.assert_not_called()
    def test_pending_order_skips_before_fetch(self):
        with patch.object(e,"market_open",return_value=True),patch.object(e,"broker_snapshot",return_value=(FakeApp(),{}, {4:("UBER","Submitted")})),patch.object(e,"candidate") as candidate:
            self.assertEqual(e.run("UBER",execute=True),0)
            candidate.assert_not_called()
    def test_not_in_watchlist_blocked(self):
        with self.assertRaises(RuntimeError): e.run("NOT_A_STOCK",execute=True)
    def test_sleeve_only_counts_recorded_holdings(self):
        with tempfile.TemporaryDirectory() as root, patch.object(e,"STATE",Path(root)):
            (Path(root)/"trades.jsonl").write_text(json.dumps({"strategy":"WYCKOFF-RISK025","status":"Filled","symbol":"ABC","quantity":10,"timestampUtc":"2026-10-29T12:00:00+00:00"})+"\n")
            p={(e.ACCOUNT,"ABC"):(10,100,"STK","USD"),(e.ACCOUNT,"LEGACY"):(1000,100,"STK","USD")}
            self.assertEqual(e.sleeve_exposure(p),1000)
            p[(e.ACCOUNT,"ABC")]=(11,100,"STK","USD")
            with self.assertRaises(RuntimeError):e.sleeve_exposure(p)

if __name__=="__main__":unittest.main()
