from typing import Any


def notification_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    status = "approved" if state.get("approved", False) else "pending approval"
    comments = f"Notification: request status is {status}."
    return {"comments": comments}
