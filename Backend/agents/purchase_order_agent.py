from typing import Any


def purchase_order_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    approved = state.get("approved", False)
    comments = (
        f"Purchase order approved for {state.get('item', 'item')}" if approved else "Purchase order rejected."
    )
    return {"comments": comments}
