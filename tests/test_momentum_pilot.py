import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import momentum_pilot as m


class PilotTests(unittest.TestCase):
    def test_duplicate_intent_ids_block_even_when_resolved(self):
        rows = [{'event': 'intent', 'id': 3}, {'event': 'resolved', 'id': 3}, {'event': 'intent', 'id': 3}]
        with self.assertRaisesRegex(RuntimeError, 'duplicate'):
            m.inventory(rows, {}, '2026-10-30')
        rows[0]['intent_id'], rows[2]['intent_id'] = 'first', 'second'
        with self.assertRaisesRegex(RuntimeError, 'unresolved'):
            m.inventory(rows, {}, '2026-10-30')

    def test_execution_filters_and_end_barrier(self):
        class App:
            def execDetails(self, *args): pass
            def execDetailsEnd(self, *args): pass
            def reqExecutions(self, request, filt):
                self.assert_account = filt.acctCode
                contract = SimpleNamespace(symbol='GM', secType='STK', currency='USD')
                def send(**kwargs):
                    fields = dict(acctNumber=m.ACCOUNT, orderRef='unique', orderId=8,
                                  side='BOT', execId='one', shares=2)
                    fields.update(kwargs)
                    self.execDetails(request, contract, SimpleNamespace(**fields))
                send(); send()  # duplicate execId is one fill
                for change in ({'acctNumber': 'OTHER'}, {'orderRef': m.REF},
                               {'orderId': 9}, {'side': 'SLD'}): send(**change)
                self.execDetailsEnd(request + 1)
                self.execDetailsEnd(request)
        app = App()
        self.assertEqual(m.execution_snapshot(app, 8, 'GM', 'BUY', 'unique'), 2)
        self.assertEqual(app.assert_account, m.ACCOUNT)

    def test_execution_end_missing_blocks(self):
        class App:
            def execDetails(self, *args): pass
            def execDetailsEnd(self, *args): pass
            def reqExecutions(self, request, filt): pass
        with patch.object(m.threading, 'Event') as event:
            event.return_value.wait.return_value = False
            with self.assertRaisesRegex(RuntimeError, 'incomplete'):
                m.execution_snapshot(App(), 8, 'GM', 'BUY', 'unique')

    def test_submit_cancel_partial_and_zero_and_pending(self):
        class App:
            next_order_id = 8
            order_results = {8: {'status': 'Submitted'}}
            def placeOrder(self, oid, contract, order): self.ref = order.orderRef
            def cancelOrder(self, oid): self.order_results[oid] = {'status': 'Cancelled'}
            def disconnect(self): pass
        rows = []
        app = App()
        with patch.object(m, 'append', side_effect=rows.append), patch.object(m, 'broker_snapshot') as snapshot, patch.object(m, 'execution_snapshot', return_value=2) as executions, patch('time.sleep'):
            snapshot.return_value = (App(), {(m.ACCOUNT, 'GM'): (2, 40, 'STK', 'USD')}, {})
            self.assertEqual(m.submit(app, 'GM', 'BUY', 5, 40, 0), 2)
            self.assertEqual(executions.call_args.args[-1], app.ref)
        self.assertEqual([r['event'] for r in rows], ['intent', 'fill', 'resolved'])
        self.assertNotEqual(rows[0]['intent_id'], m.REF)
        rows.clear()
        app = App()
        with patch.object(m, 'append', side_effect=rows.append), patch.object(m, 'broker_snapshot', return_value=(App(), {}, {})), patch.object(m, 'execution_snapshot', return_value=0), patch('time.sleep'):
            self.assertEqual(m.submit(app, 'GM', 'BUY', 5, 40, 0), 0)
        self.assertEqual([r['event'] for r in rows], ['intent', 'resolved'])
        rows.clear()
        app = App()
        with patch.object(m, 'append', side_effect=rows.append), patch.object(m, 'broker_snapshot', return_value=(App(), {}, {8: ('GM', 'Submitted')})), patch('time.sleep'):
            with self.assertRaisesRegex(RuntimeError, 'resting order'):
                m.submit(app, 'GM', 'BUY', 5, 40, 0)
        self.assertEqual([r['event'] for r in rows], ['intent'])
        rows.clear()
        app = App()
        with patch.object(m, 'append', side_effect=rows.append), patch.object(m, 'broker_snapshot', return_value=(App(), {(m.ACCOUNT, 'GM'): (2, 40, 'STK', 'USD')}, {})), patch.object(m, 'execution_snapshot', return_value=1), patch('time.sleep'):
            with self.assertRaisesRegex(RuntimeError, 'execution/position'):
                m.submit(app, 'GM', 'BUY', 5, 40, 0)
        self.assertEqual([r['event'] for r in rows], ['intent'])

    def test_unresolved_intent_blocks(self):
        with self.assertRaisesRegex(RuntimeError, 'unresolved'):
            m.inventory([{'event': 'intent', 'id': 2}], {}, '2026-10-30')

    def test_partial_fill_owned_and_cap(self):
        rows = [{'event': 'intent', 'id': 2}, {'event': 'fill', 'id': 2, 'symbol': 'GM', 'side': 'BUY', 'qty': 3, 'day': '2026-10-30'}, {'event': 'resolved', 'id': 2}]
        owned, daily = m.inventory(rows, {(m.ACCOUNT, 'GM'): (3, 40, 'STK', 'USD')}, '2026-10-30')
        self.assertEqual(owned, {'GM': 3})
        self.assertEqual(daily, {'GM'})
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            m.inventory(rows, {(m.ACCOUNT, 'GM'): (4, 40, 'STK', 'USD')}, '2026-10-30')

    def test_unmatched_broker_position_not_entry(self):
        positions = {(m.ACCOUNT, 'GM'): (5, 40, 'STK', 'USD')}
        self.assertTrue(any(s == 'GM' for _, s in positions))
        with self.assertRaisesRegex(RuntimeError, 'mismatch'):
            m.inventory([{'event': 'fill', 'symbol': 'GM', 'side': 'BUY', 'qty': 2}], positions, '2026-10-30')

    def test_stale_quote_blocks(self):
        old = (datetime.now(timezone.utc) - timedelta(minutes=4)).isoformat()
        with patch.object(m, 'fetch_quotes', return_value=({'GM': {'bid': 99.9, 'ask': 100, 'timestamp': old}}, None)):
            with self.assertRaisesRegex(RuntimeError, 'stale'):
                m.quote('GM', 100)

    def test_missed_close_alerts_no_order(self):
        now = datetime(2026, 10, 30, 21, 0, tzinfo=timezone.utc)
        class App:
            def disconnect(self): pass
        with patch.object(m, 'broker_snapshot', return_value=(App(), {}, {})), patch.object(m, 'session', return_value=False), patch.object(m, 'STATE', Path('/tmp')), patch.object(m, 'LEDGER', Path('/nonexistent-momentum-ledger')):
            self.assertEqual(m.run(False, now), 0)

    def test_default_dry_run_and_ref(self):
        self.assertEqual(m.run.__defaults__[0], False)
        self.assertEqual(m.REF, 'EXP-INTRADAY-MOMENTUM')


if __name__ == '__main__':
    unittest.main()
