from typing import Any


def request_parser_agent(state: dict[str, Any], runtime) -> dict[str, Any]:
    return {
        "employee": state.get("employee", ""),
        "item": state.get("item", ""),
        "quantity": state.get("quantity", 0),
        "price": state.get("price", 0.0),
        "vendor": state.get("vendor", ""),
        "approved": state.get("approved", False),
        "comments": state.get("comments", "Parsed request data."),
    }
