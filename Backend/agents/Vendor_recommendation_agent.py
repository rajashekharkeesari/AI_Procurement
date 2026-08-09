from typing import Any


def vendor_recommendation_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    recommended = state.get("approved", False)
    comments = (
        f"Vendor {state.get('vendor', 'unknown')} is recommended for {state.get('item', 'item')}"
        if recommended
        else f"Vendor recommendation withheld because the request is not approved."
    )
    return {"comments": comments}
