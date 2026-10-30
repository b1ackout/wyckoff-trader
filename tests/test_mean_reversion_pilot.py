import sys
import unittest
from datetime import datetime, date, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import mean_reversion_pilot as m


class MeanReversionTests(unittest.TestCase):
    def test_completed_previous_day_and_stale(self):
        now = datetime(2026, 10, 30, 15, tzinfo=timezone.utc)
        stamps = [datetime(2026, 10, d, 12, tzinfo=timezone.utc) for d in (28, 29, 30)]
        self.assertEqual(m.completed_daily([80, 90, 120], stamps, now), ([80., 90.], 90.))
        with self.assertRaisesRegex(RuntimeError, 'stale'):
            m.completed_daily([80], [stamps[0]], now)
        with self.assertRaisesRegex(RuntimeError, 'stale'):
            m.completed_daily([80], [datetime(2026, 10, 23, 12, tzinfo=timezone.utc)], now)
        with self.assertRaisesRegex(RuntimeError, 'naive'):
            m.completed_daily([90], [datetime(2026, 10, 29)], now)

    def test_no_duplicate_any_strategy(self):
        self.assertFalse(m.entry_allowed('GM', {(m.ACCOUNT, 'GM'): (3, 40, 'STK', 'USD')}, {}, {}, set()))
        self.assertFalse(m.entry_allowed('GM', {}, {1: ('GM', 'Submitted')}, {}, set()))
        self.assertFalse(m.entry_allowed('GM', {}, {}, {'GM': 2}, set()))
        self.assertTrue(m.entry_allowed('GM', {}, {}, {}, set()))

    def test_partial_fill_owned(self):
        rows = [{'event': 'intent', 'id': 8, 'intent_id': 'ref'},
                {'event': 'fill', 'id': 8, 'symbol': 'GM', 'side': 'BUY', 'qty': 2, 'day': '2026-10-30'},
                {'event': 'resolved', 'id': 8, 'intent_id': 'ref'}]
        owned, daily = m.inventory(rows, {(m.ACCOUNT, 'GM'): (2, 40, 'STK', 'USD')}, '2026-10-30')
        self.assertEqual((owned, daily), ({'GM': 2}, {'GM'}))
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            m.inventory(rows, {(m.ACCOUNT, 'GM'): (3, 40, 'STK', 'USD')}, '2026-10-30')

    def test_five_trading_day_exit_and_thresholds(self):
        entry = date(2026, 10, 23)
        self.assertFalse(m.exit_trigger(100, 100, entry, datetime(2026, 10, 29, 15, tzinfo=timezone.utc)))
        self.assertTrue(m.exit_trigger(100, 100, entry, datetime(2026, 10, 30, 15, tzinfo=timezone.utc)))
        self.assertTrue(m.exit_trigger(96, 100, date(2026, 10, 29), datetime(2026, 10, 30, 15, tzinfo=timezone.utc)))
        self.assertTrue(m.exit_trigger(106, 100, date(2026, 10, 29), datetime(2026, 10, 30, 15, tzinfo=timezone.utc)))

    def test_partial_fill_cancel_and_nonterminal_block(self):
        class App:
            next_order_id=8
            def __init__(self): self.order_results={8:{'status':'Submitted'}}
            def placeOrder(self,oid,contract,order): self.ref=order.orderRef
            def cancelOrder(self,oid): self.order_results[oid]={'status':'Cancelled'}
            def disconnect(self): pass
        app=App()
        rows=[]
        with patch.object(m,'append',side_effect=rows.append), patch.object(m,'broker_snapshot') as snapshot, patch.object(m,'execution_snapshot',return_value=2), patch('time.sleep'):
            snapshot.return_value=(App(),{(m.ACCOUNT,'GM'):(2,40,'STK','USD')},{})
            self.assertEqual(m.submit(app,'GM','BUY',5,40,0),2)
        self.assertEqual([r['event'] for r in rows],['intent','fill','resolved'])
        app=App(); app.cancelOrder=lambda oid: None
        rows=[]
        with patch.object(m,'append',side_effect=rows.append), patch.object(m,'broker_snapshot') as snapshot, patch.object(m,'execution_snapshot',return_value=2), patch('time.sleep'):
            snapshot.return_value=(App(),{(m.ACCOUNT,'GM'):(2,40,'STK','USD')},{})
            with self.assertRaisesRegex(RuntimeError,'not terminal'):
                m.submit(app,'GM','BUY',5,40,0)
        self.assertEqual([r['event'] for r in rows],['intent'])
    def test_reopened_lot_resets_holding_day(self):
        rows=[{'event':'fill','symbol':'GM','side':'BUY','qty':5,'day':'2026-10-10'},
              {'event':'fill','symbol':'GM','side':'SELL','qty':5,'day':'2026-10-12'},
              {'event':'fill','symbol':'GM','side':'BUY','qty':2,'day':'2026-10-29'}]
        self.assertEqual(m.first_entry(rows,'GM'),date(2026,10,29))
    def test_dry_run_and_distinct_ledger(self):
        self.assertFalse(m.run.__defaults__[0])
        self.assertEqual(m.LEDGER.name, 'mean_reversion.jsonl')
        self.assertEqual(m.REF, 'EXP-MEAN-REVERSION')


if __name__ == '__main__': unittest.main()
