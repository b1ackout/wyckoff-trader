import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from risk_sizing import proposed_shares

class RiskSizingTests(unittest.TestCase):
    def test_200_dollar_risk_long(self):
        r=proposed_shares(80000,100,92,0,80000)
        self.assertEqual((r["risk_budget_usd"],r["proposed_shares"]),(200,25))
    def test_existing_exposure_blocks(self):
        r=proposed_shares(80000,100,92,90000,80000)
        self.assertEqual(r["proposed_shares"],0)
    def test_short_direction(self):
        self.assertEqual(proposed_shares(80000,100,108,0,80000,"SHORT")["proposed_shares"],25)
        with self.assertRaises(ValueError):proposed_shares(80000,100,92,0,80000,"SHORT")

if __name__=="__main__":unittest.main()
