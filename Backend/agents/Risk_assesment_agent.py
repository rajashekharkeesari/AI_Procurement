from typing import Any


def risk_assessment_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    approved = state.get("approved", False)
    risk = "low" if approved else "high"
    comments = f"Risk assessment: {risk} risk."
    return {"comments": comments}
