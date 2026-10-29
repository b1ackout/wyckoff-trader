import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scheduled_check as s

class Result:
    def __init__(self, code, output):
        self.returncode, self.stdout, self.stderr = code, output, ""

class ScheduledCheckTests(unittest.TestCase):
    def run_with(self, manager):
        with patch.object(s, "run_script", side_effect=[Result(0, "30 names scanned"), manager]) as run, contextlib.redirect_stdout(io.StringIO()) as output:
            status = s.main()
        self.assertEqual(run.call_count, 2)
        self.assertIn("READ-ONLY SCAN", output.getvalue())
        return status, output.getvalue()
    def test_known_broker_outage_is_visible_noop(self):
        status, output = self.run_with(Result(2, "BLOCK: RuntimeError paper account connection/identity unavailable"))
        self.assertEqual(status, 0)
        self.assertIn("BROKER_UNAVAILABLE", output)
    def test_unknown_order_state_is_real_failure(self):
        status, output = self.run_with(Result(2, "ORDER STATUS UNKNOWN paper account connection/identity unavailable"))
        self.assertEqual(status, 2)
        self.assertIn("EXIT_MANAGER_FAILED", output)
    def test_unclassified_failure_remains_failure(self):
        status, _ = self.run_with(Result(2, "position/order inventory changed"))
        self.assertEqual(status, 2)
    def test_successful_exit_check_runs_one_capped_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0, "scan"), Result(0, "No executable exit signals"), Result(0, "SKIP no eligible new experiment candidate"), Result(0, "SHADOW 8 symbols 0 signals")]) as run, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 4)
        self.assertEqual(run.call_args_list[-2].args, ("experiment_entry.py", ("--auto", "--execute")))
        self.assertIn("PILOT ENTRY", out.getvalue())
    def test_exit_order_skips_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0, "scan"), Result(0, "ORDER 1 BUY 10")]) as run:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 2)

if __name__ == "__main__": unittest.main()
