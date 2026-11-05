import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import research_store as r

class StoreTests(unittest.TestCase):
    def test_completed_bars_only_and_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            with r.connect(Path(d)/'r.sqlite3') as db:
                row = dict(t='2026-11-04',o=10,h=12,l=9,c=11,v=100)
                bars={'ABC':[row,{**row,'t':'2026-11-05','c':11}]}
                self.assertEqual(r.save_bars(db,bars,'now','2026-11-05'),1)
                self.assertEqual(r.save_bars(db,bars,'later','2026-11-05'),0)
                self.assertEqual(db.execute('SELECT count(*) FROM daily_bars').fetchone()[0],1)
    def test_execution_dedup_and_paper_gate(self):
        with tempfile.TemporaryDirectory() as d:
            with r.connect(Path(d)/'r.sqlite3') as db:
                row=dict(account=r.ACCOUNT,exec_id='id1',symbol='ABC',security_type='STK',currency='USD',side='BOT',shares=2,price=10,executed_at='20261105 10:00:00',order_id=1,perm_id=5,order_ref='',exchange='NYSE')
                self.assertEqual(r.save_executions(db,[row],'now'),1)
                self.assertEqual(r.save_executions(db,[row],'later'),1)
                with self.assertRaises(ValueError):r.save_executions(db,[{**row,'account':'LIVE'}],'now')
                self.assertEqual(db.execute('SELECT count(*) FROM executions').fetchone()[0],1)

if __name__=='__main__': unittest.main()
