from typing import Any


def Human_approval_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    approved = state.get("approved", False)
    comments = (
        "Human approval received." if approved else "Human approval required."
    )
    return {"approved": approved, "comments": comments}
