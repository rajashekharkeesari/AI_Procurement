"""
Vendor Recommendation Agent

Recommends the best (cheapest) vendor for a procurement request.
If multiple vendors supply the same item, picks the one with the lowest price.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm
from Backend.Database import SessionLocal
from Backend.repositories.vendors import get_cheapest_vendor_for_item
from Backend.repositories.stationary import get_stationary_by_name


SYSTEM_PROMPT = """You are the Vendor Recommendation Agent in a procurement workflow.
You are given vendor comparison data. Summarize why the chosen vendor was selected.

If multiple vendors were available, explain that the cheapest was chosen.
If only one vendor is available, confirm it.
If no vendor was found, state that.

Keep it brief. Do NOT call any tools."""


def vendor_recommendation_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Recommend the cheapest vendor for the requested item.
    """
    item_name = state.get("item", "")
    preferred_vendor = state.get("vendor", "")

    # Look up the stationary item and find cheapest vendor
    vendor_info = None
    db = SessionLocal()
    try:
        item_record = get_stationary_by_name(db, item_name)
        if item_record:
            vendor_info = get_cheapest_vendor_for_item(db, item_record["id"])
    finally:
        db.close()

    # Build context for LLM
    if vendor_info:
        all_vendors_text = "\n".join(
            f"  - {v['name']}: ${v['price']}" if v['price'] else f"  - {v['name']}: no price set"
            for v in vendor_info["all_vendors"]
        )
        chosen = vendor_info["name"]
        chosen_price = vendor_info["price"]

        vendor_context = (
            f"Available vendors for '{item_name}':\n{all_vendors_text}\n\n"
            f"CHOSEN (lowest price): {chosen} at ${chosen_price}\n"
            f"Preferred vendor from request: {preferred_vendor or 'none specified'}"
        )

        # Update state with the chosen vendor
        recommended_vendor = chosen
    else:
        vendor_context = (
            f"No vendors found for item '{item_name}'.\n"
            f"Preferred vendor from request: {preferred_vendor or 'none specified'}\n"
            f"Using preferred vendor if specified."
        )
        recommended_vendor = preferred_vendor or "Unknown"

    llm = create_llm()

    user_content = (
        f"Vendor recommendation:\n"
        f"{vendor_context}\n\n"
        f"Provide a brief summary of the recommendation."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    return {
        "vendor": recommended_vendor,
        "comments": f"Vendor: {recommended_vendor}. {response.content}",
    }
