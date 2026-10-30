import sys
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import shadow_experiments as s

class ShadowSignalTests(unittest.TestCase):
    def test_momentum_requires_breakout_and_volume(self):
        closes=[10.0]*20+[11.0];highs=[10.1]*20+[11.1];volumes=[100]*20+[130]
        self.assertTrue(s.intraday_momentum(closes,highs,volumes))
        volumes[-1]=100
        self.assertFalse(s.intraday_momentum(closes,highs,volumes))
    def test_insufficient_data_never_signals(self):
        self.assertFalse(s.intraday_momentum([1],[1],[100]))
        self.assertFalse(s.daily_mean_reversion([1]*20))
    def test_intraday_rejects_old_and_forming_candles(self):
        now=datetime(2026,10,30,15,20,tzinfo=timezone.utc)
        et=ZoneInfo("America/New_York")
        self.assertTrue(s.fresh_intraday_bar(now-timedelta(minutes=10), now))
        self.assertFalse(s.fresh_intraday_bar(now-timedelta(minutes=2), now))
        self.assertFalse(s.fresh_intraday_bar(now-timedelta(hours=20), now))
        self.assertFalse(s.fresh_intraday_bar(now-timedelta(minutes=25), now))
        self.assertFalse(s.fresh_intraday_bar(now.replace(hour=6).astimezone(et), now))

if __name__=="__main__":unittest.main()
