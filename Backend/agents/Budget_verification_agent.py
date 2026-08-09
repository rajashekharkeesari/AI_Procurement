from typing import Any


def Budget_verification_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    total_cost = state.get("quantity", 0) * state.get("price", 0.0)
    approved = total_cost <= 10000.0
    comments = (
        f"Budget verification passed: total cost ${total_cost:.2f}."
        if approved
        else f"Budget verification failed: total cost ${total_cost:.2f} exceeds threshold."
    )
    return {"approved": approved, "comments": comments}
