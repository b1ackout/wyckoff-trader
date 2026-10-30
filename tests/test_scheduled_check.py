import contextlib
import fcntl
import io
import sys
import tempfile
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
        with patch.object(s, "run_script", side_effect=[Result(0, "scan"), Result(0, "No executable exit signals"), Result(0, "No eligible momentum entry"), Result(0, "No eligible mean-reversion entry"), Result(0, "SKIP no eligible new experiment candidate"), Result(0, "SHADOW 8 symbols 0 signals")]) as run, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 6)
        self.assertEqual(run.call_args_list[2].args, ("momentum_pilot.py", ("--execute",)))
        self.assertEqual(run.call_args_list[3].args, ("mean_reversion_pilot.py", ("--execute",)))
        self.assertEqual(run.call_args_list[-2].args, ("experiment_entry.py", ("--auto", "--execute")))
        self.assertIn("PILOT ENTRY", out.getvalue())
    def test_momentum_action_skips_wyckoff_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0,"scan"), Result(0,"No executable exit signals"), Result(0,"BROKER_ACTION BUY GM 2")]) as run:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 3)
    def test_momentum_broker_error_blocks_wyckoff_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0,"scan"), Result(0,"No executable exit signals"), Result(2,"BLOCK unresolved order intent")]) as run:
            self.assertEqual(s.main(), 2)
        self.assertEqual(run.call_count, 3)
    def test_mean_order_skips_wyckoff_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0,"scan"), Result(0,"No executable exit signals"), Result(0,"No eligible momentum entry"), Result(0,"BROKER_ACTION BUY PYPL 2")]) as run:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 4)
    def test_mean_error_blocks_wyckoff_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0,"scan"), Result(0,"No executable exit signals"), Result(0,"No eligible momentum entry"), Result(2,"BLOCK unresolved order intent")]) as run:
            self.assertEqual(s.main(), 2)
        self.assertEqual(run.call_count, 4)
    def test_exit_order_skips_entry(self):
        with patch.object(s, "run_script", side_effect=[Result(0, "scan"), Result(0, "ORDER 1 BUY 10")]) as run:
            self.assertEqual(s.main(), 0)
        self.assertEqual(run.call_count, 2)
    def test_busy_cycle_never_starts_broker_check(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(s.Path, "home", return_value=Path(directory)):
            state = Path(directory)/".openclaw/state/wyckoff-experiments"
            state.mkdir(parents=True)
            with (state/"cycle.lock").open("a") as held, patch.object(s, "_cycle") as cycle:
                fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.assertEqual(s.main(), 0)
                cycle.assert_not_called()

if __name__ == "__main__": unittest.main()
