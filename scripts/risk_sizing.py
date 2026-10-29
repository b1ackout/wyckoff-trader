"""Pure paper-trade sizing simulation; does not submit orders."""
import math

RISK_FRACTION = 0.0025


def proposed_shares(capital_usd, entry, stop, gross_exposure_usd, gross_cap_usd, side="LONG"):
    """Fail closed unless both planned stop risk and portfolio gross exposure fit."""
    vals = (capital_usd, entry, stop, gross_exposure_usd, gross_cap_usd)
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("all inputs must be finite")
    if capital_usd <= 0 or entry <= 0 or stop <= 0 or side not in ("LONG", "SHORT"):
        raise ValueError("invalid capital, price, stop, or side")
    if (side == "LONG" and stop >= entry) or (side == "SHORT" and stop <= entry):
        raise ValueError("stop must be on the losing side of entry")
    if gross_exposure_usd < 0 or gross_cap_usd <= 0:
        raise ValueError("invalid gross portfolio exposure/cap")
    risk_dollars = capital_usd * RISK_FRACTION
    stop_distance = abs(entry - stop)
    remaining = max(0, gross_cap_usd - gross_exposure_usd)
    return {
        "risk_budget_usd": risk_dollars,
        "shares_by_stop": math.floor(risk_dollars / stop_distance),
        "shares_by_cap": math.floor(remaining / entry),
        "proposed_shares": max(0, min(math.floor(risk_dollars / stop_distance), math.floor(remaining / entry))),
    }
