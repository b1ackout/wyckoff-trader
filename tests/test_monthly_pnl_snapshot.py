import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import monthly_pnl_snapshot as m

def row(event,day,stamp,nlv,realized,unrealized):
    return {'event':event,'account':m.ACCOUNT,'date_et':day,'timestamp_utc':stamp,'currency':'EUR','net_liquidation':nlv,'realized_daily_pnl_base':realized,'unrealized_pnl_base':unrealized}

class MonthlyPnlTests(unittest.TestCase):
    def test_baseline_day_realized_delta_and_open_pnl_change(self):
        rows=[row('baseline','2026-11-03','2026-11-03T18:00:00+00:00',1000,2,100),row('snapshot','2026-11-03','2026-11-03T22:00:00+00:00',1010,4,110),row('snapshot','2026-11-04','2026-11-04T22:00:00+00:00',1022,5,120)]
        s=m.summarize_month(rows,'2026-11')
        self.assertEqual(s['realized_pnl_observed'],7)
        self.assertEqual(s['unrealized_change'],20)
        self.assertEqual(s['total_pnl_estimate'],27)
        self.assertEqual(s['net_liquidation_change_before_external_flows'],22)
        self.assertEqual(s['baseline_source'],'explicit starting baseline')
        self.assertEqual(s['reconciliation_status'],'MATCH')

    def test_previous_month_snapshot_is_baseline(self):
        rows=[{'event':'snapshot','account':m.ACCOUNT,'date_et':'2026-10-31','timestamp_utc':'2026-10-31T22:00:00+00:00','currency':'EUR','net_liquidation':900,'realized_daily_pnl':0,'unrealized_pnl':-500},row('snapshot','2026-10-30','2026-10-30T22:00:00+00:00',1000,0,90),row('snapshot','2026-11-02','2026-11-02T22:00:00+00:00',1015,3,100)]
        s=m.summarize_month(rows,'2026-11')
        self.assertEqual(s['realized_pnl_observed'],3)
        self.assertEqual(s['unrealized_change'],10)
        self.assertEqual(s['total_pnl_estimate'],13)
        self.assertEqual(s['baseline_date_et'],'2026-10-30')

    def test_large_difference_is_flagged_for_review(self):
        rows=[row('baseline','2026-11-03','2026-11-03T18:00:00+00:00',1000,0,100),row('snapshot','2026-11-04','2026-11-04T22:00:00+00:00',1000,0,500)]
        self.assertEqual(m.summarize_month(rows,'2026-11')['reconciliation_status'],'REVIEW')

    def test_latest_starting_baseline_supersedes_earlier_reading(self):
        rows=[row('baseline','2026-11-03','2026-11-03T18:00:00+00:00',1000,0,-2500),row('snapshot','2026-11-03','2026-11-03T18:10:00+00:00',1000,0,7900),row('baseline','2026-11-03','2026-11-03T18:20:00+00:00',1000,0,7900)]
        s=m.summarize_month(rows,'2026-11')
        self.assertEqual(s['baseline_source'],'explicit starting baseline')
        self.assertEqual(s['unrealized_change'],0)
        self.assertEqual(s['reconciliation_status'],'MATCH')

    def test_no_data_is_explicit(self):
        self.assertIsNone(m.summarize_month([], '2026-11'))

if __name__=='__main__':unittest.main()
