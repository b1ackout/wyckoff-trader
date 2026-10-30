#!/usr/bin/env python3
"""Run the paper scan and guarded exits; keep a TWS outage visible without auto-disabling the scheduler."""
import subprocess
import sys
import fcntl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
KNOWN_BROKER_BLOCKS = (
    "paper account connection/identity unavailable",
    "broker position/open-order inventory incomplete",
)


def run_script(name, args=(), timeout=45):
    try:
        return subprocess.run([PYTHON, str(ROOT / "scripts" / name), *args],
                              capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        print(f"{name}: timed out; broker action state may be unknown. Inspect TWS before retrying.")
        return None


def _cycle():
    scan = run_script("scan_watchlist.py")
    if scan is None: return 2
    print("=== READ-ONLY SCAN ===")
    print(scan.stdout.strip())
    if scan.returncode:
        print("SCAN_FAILED:", scan.stderr[-1000:]); return 2
    manager = run_script("manage_positions.py", ("--execute",))
    if manager is None: return 2
    print("=== PAPER EXIT MANAGER ===")
    print(manager.stdout.strip())
    if manager.returncode == 0:
        # Avoid opening a new experiment position in a cycle that just closed one.
        if "ORDER " in manager.stdout or "ORDER STATUS UNKNOWN" in manager.stdout:
            print("ENTRY_SKIP: broker exit action requires reconciliation first")
            return 0
        momentum = run_script("momentum_pilot.py", ("--execute",), timeout=90)
        if momentum is None: return 2
        print("=== INTRADAY MOMENTUM PAPER PILOT ===")
        print(momentum.stdout.strip())
        if momentum.returncode:
            if any(reason in momentum.stdout for reason in KNOWN_BROKER_BLOCKS) and "BROKER_ACTION" not in momentum.stdout:
                print("BROKER_UNAVAILABLE: momentum exit and entry checks were not completed; no momentum order submitted")
                return 0
            print("MOMENTUM_FAILED: inspect broker orders and momentum ledger before retrying")
            return 2
        if "BROKER_ACTION" in momentum.stdout:
            print("WYCKOFF_ENTRY_SKIP: momentum broker action requires reconciliation first")
            return 0
        mean = run_script("mean_reversion_pilot.py", timeout=90)
        if mean is None: return 2
        print("=== MEAN REVERSION PAPER PILOT ===")
        print(mean.stdout.strip())
        if mean.returncode:
            if any(reason in mean.stdout for reason in KNOWN_BROKER_BLOCKS) and "BROKER_ACTION" not in mean.stdout:
                print("BROKER_UNAVAILABLE: mean-reversion exit and entry checks were not completed; no mean-reversion order submitted")
                return 0
            print("MEAN_REVERSION_FAILED: inspect broker orders and mean-reversion ledger before retrying")
            return 2
        if "BROKER_ACTION" in mean.stdout:
            print("WYCKOFF_ENTRY_SKIP: mean-reversion broker action requires reconciliation first")
            return 0
        entry = run_script("experiment_entry.py", ("--auto", "--execute"))
        if entry is None: return 2
        print("=== WYCKOFF RISK-025 PILOT ENTRY ===")
        print(entry.stdout.strip())
        if entry.returncode == 0:
            shadow = run_script("shadow_experiments.py", timeout=25)
            print("=== SHADOW STRATEGY SIGNALS (NO ORDERS) ===")
            if shadow is None:
                print("SHADOW_UNAVAILABLE: market data timed out; paper exit/entry results above remain valid")
            elif shadow.returncode:
                print("SHADOW_UNAVAILABLE:", shadow.stderr[-300:])
            else:
                print(shadow.stdout.strip())
            return 0
        if any(reason in entry.stdout for reason in KNOWN_BROKER_BLOCKS) and "ORDER STATUS UNKNOWN" not in entry.stdout:
            print("BROKER_UNAVAILABLE: no pilot entry; next scan remains scheduled.")
            return 0
        print("ENTRY_FAILED: inspect TWS orders before retrying.")
        print(entry.stderr[-1000:])
        return 2
    if any(reason in manager.stdout for reason in KNOWN_BROKER_BLOCKS) and "ORDER STATUS UNKNOWN" not in manager.stdout:
        print("BROKER_UNAVAILABLE: no order submitted; scan continues next run. Restore TWS for exits.")
        return 0
    print("EXIT_MANAGER_FAILED: inspect TWS order state before retrying.")
    print(manager.stderr[-1000:])
    return 2


def main():
    state = Path.home() / ".openclaw/state/wyckoff-experiments"
    state.mkdir(parents=True, exist_ok=True)
    with (state / "cycle.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("CYCLE_BUSY: another scheduled paper cycle owns the broker checks; no duplicate cycle")
            return 0
        return _cycle()


if __name__ == "__main__":
    raise SystemExit(main())
