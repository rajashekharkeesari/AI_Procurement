"""
Notification Agent

Generates notifications about the procurement request status.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm


SYSTEM_PROMPT = """You are the Notification Agent in a procurement workflow.
Generate a clear, professional notification about the procurement request status.

Include:
1. Address the requesting employee by name.
2. State the final status (approved/rejected/ordered).
3. Summarize key details (item, quantity, total cost).
4. Mention next steps if applicable.

Keep it concise and professional.

Do NOT call any tools."""


def notification_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a notification about request status.
    """
    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))
    status = state.get("status", "pending")

    llm = create_llm()

    user_content = (
        f"Generate a notification for this procurement request:\n"
        f"Employee: {state.get('employee', 'unknown')}\n"
        f"Item: {state.get('item', 'unknown')}\n"
        f"Quantity: {state.get('quantity', 0)}\n"
        f"Unit Price: ${state.get('price', 0.0):.2f}\n"
        f"Total Cost: ${total_cost:.2f}\n"
        f"Vendor: {state.get('vendor', 'unknown')}\n"
        f"Final Status: {status}\n"
        f"Purchase Order ID: {state.get('purchase_order_id', 'N/A')}\n"
        f"Previous Comments: {state.get('comments', 'none')}"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    return {
        "notification": response.content,
        "status": status,
    }
