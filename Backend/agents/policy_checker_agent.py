from typing import Any


def policy_checker_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    quantity = state.get("quantity", 0)
    policy_limit = 10000.0
    approved = quantity * state.get("price", 0.0) <= policy_limit
    comments = (
        "Policy compliance passed." if approved else "Policy compliance failed."
    )
    return {"approved": approved, "comments": comments}
