import sys
import unittest
from unittest.mock import patch
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import manage_positions as m

class ExitPolicyTests(unittest.TestCase):
    def test_long_loss_and_profit(self):
        self.assertIn("8%", m.exit_reason(100, 100, 91.99))
        self.assertIn("12%", m.exit_reason(100, 100, 112.01))
        self.assertIsNone(m.exit_reason(100, 100, 102))
    def test_short_loss_and_profit(self):
        self.assertIn("8%", m.exit_reason(-100, 100, 108.01))
        self.assertIn("12%", m.exit_reason(-100, 100, 87.99))
    def test_two_timeframe_opposition_only(self):
        self.assertIsNone(m.exit_reason(100, 100, 99, "SHORT", "NEUTRAL", "NEUTRAL"))
        self.assertIn("opposite", m.exit_reason(100, 100, 99, "SHORT", "SHORT", "NEUTRAL"))
        self.assertIn("opposite", m.exit_reason(-100, 100, 101, "LONG", "LONG", "NEUTRAL"))
    def test_invalid_price_blocks(self):
        self.assertIsNone(m.exit_reason(100, 0, 100))
        self.assertIsNone(m.exit_reason(100, 100, float("nan")))
    def test_market_hours(self):
        ny=ZoneInfo("America/New_York")
        self.assertFalse(m.market_open(datetime(2026,10,28,16,10,tzinfo=ny)))
        self.assertTrue(m.market_open(datetime(2026,10,28,12,0,tzinfo=ny)))

    def test_second_snapshot_uses_new_client_and_blocks_pending_orders(self):
        class App:
            def disconnect(self): pass
        held = {(m.ACCOUNT, "F"): (100, 120, "STK", "USD")}
        calls = []
        def snapshot(client_id=78):
            calls.append(client_id)
            return App(), held, {} if client_id == 78 else {55: ("F", "Submitted")}
        bars = [{"c": 100}] * 25
        with patch.object(m, "broker_snapshot", side_effect=snapshot), \
             patch.object(m, "download_batch", return_value={"F": bars}), \
             patch.object(m, "fetch_quotes", return_value=({"F": {"bid": 100, "ask": 100.05}}, None)), \
             patch.object(m, "quote_quality", return_value=(.0005, "OK")), \
             patch.object(m.trader, "analyze_wyckoff_multitf", return_value=("NEUTRAL", "", {"daily": "NEUTRAL", "weekly": "NEUTRAL", "monthly": "NEUTRAL"})), \
             patch.object(m, "market_open", return_value=True), \
             patch.object(m, "submit_exit") as submit:
            self.assertEqual(m.run(execute=True), 2)
            self.assertEqual(calls, [78, 79])
            submit.assert_not_called()

if __name__ == "__main__": unittest.main()
