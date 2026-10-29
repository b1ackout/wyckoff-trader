import sys
import unittest
from pathlib import Path
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

if __name__=="__main__":unittest.main()
