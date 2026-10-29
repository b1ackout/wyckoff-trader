#!/usr/bin/env python3
"""Run the paper scan and guarded exits; keep a TWS outage visible without auto-disabling the scheduler."""
import subprocess
import sys
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


def main():
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


if __name__ == "__main__":
    raise SystemExit(main())
