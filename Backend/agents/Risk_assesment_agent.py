"""
Risk Assessment Agent

Assesses the risk level of a procurement request based on
cost thresholds, quantity, and vendor information.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm


SYSTEM_PROMPT = """You are the Risk Assessment Agent in a procurement workflow.
Evaluate the risk level based on the provided data.

Risk rules:
1. Total cost > $5000 = HIGH risk
2. Total cost $1000-$5000 = MEDIUM risk
3. Total cost < $1000 = LOW risk
4. If vendor is unknown or empty, increase risk one level.
5. Large quantities (>50) may increase risk.

You MUST respond with exactly one of: LOW, MEDIUM, or HIGH as your first word.
Then provide a brief justification.

Do NOT call any tools."""


def risk_assessment_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Assess risk based on cost and vendor data.
    """
    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))
    vendor = state.get("vendor", "")

    llm = create_llm()

    user_content = (
        f"Assess the risk for this procurement request:\n"
        f"Employee: {state.get('employee', 'unknown')}\n"
        f"Item: {state.get('item', 'unknown')}\n"
        f"Quantity: {state.get('quantity', 0)}\n"
        f"Unit Price: ${state.get('price', 0.0):.2f}\n"
        f"Total Cost: ${total_cost:.2f}\n"
        f"Vendor: {vendor if vendor else 'NOT SPECIFIED'}\n"
        f"Budget Approved: {state.get('budget_sufficient', False)}"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    # Extract risk level from response
    response_text = response.content.strip()
    first_word = response_text.split()[0].upper() if response_text else "MEDIUM"

    if "HIGH" in first_word:
        risk_level = "high"
    elif "MEDIUM" in first_word or "MED" in first_word:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "comments": f"Risk Assessment ({risk_level.upper()}): {response.content}",
    }
