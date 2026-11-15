"""
Human Approval Agent

Pauses the workflow and waits for human approval from the frontend.
Uses LangGraph's interrupt mechanism to halt execution until the user
provides their decision (approve/reject) via the API.
"""

from typing import Any

from langgraph.types import interrupt
from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm


SYSTEM_PROMPT = """You are the Human Approval Agent in a procurement workflow.
Prepare a clear summary of the procurement request for a human approver.

Include:
- Who is requesting (employee name)
- What is being requested (item, quantity)
- Total cost
- Risk level and policy compliance from previous checks
- Your recommendation (approve or reject) with reasoning

Keep it concise and professional. Do NOT call any tools."""


def Human_approval_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Pause the workflow and wait for human approval.
    """
    llm = create_llm()

    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))

    user_content = (
        f"Prepare an approval summary for this procurement request:\n"
        f"Employee: {state.get('employee', 'unknown')}\n"
        f"Item: {state.get('item', 'unknown')}\n"
        f"Quantity: {state.get('quantity', 0)}\n"
        f"Unit Price: ${state.get('price', 0.0):.2f}\n"
        f"Total Cost: ${total_cost:.2f}\n"
        f"Vendor: {state.get('vendor', 'unknown')}\n"
        f"Budget Sufficient: {state.get('budget_sufficient', False)}\n"
        f"Policy Compliant: {state.get('policy_compliant', False)}\n"
        f"Risk Level: {state.get('risk_level', 'unknown')}\n"
        f"Previous Comments: {state.get('comments', 'none')}"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)
    summary = response.content

    # --- INTERRUPT: Pause workflow and wait for human input ---
    human_decision = interrupt({
        "summary": summary,
        "message": "Awaiting human approval. Please approve or reject.",
        "employee": state.get("employee", "unknown"),
        "item": state.get("item", "unknown"),
        "total_cost": total_cost,
    })

    # --- Process the human decision ---
    approved = False
    reviewer_comment = ""

    if isinstance(human_decision, dict):
        approved = human_decision.get("approved", False)
        reviewer_comment = human_decision.get("comment", "")
    elif isinstance(human_decision, bool):
        approved = human_decision
    elif isinstance(human_decision, str):
        approved = human_decision.lower() in ("approve", "approved", "yes", "true")
        reviewer_comment = human_decision

    comments = (
        f"Human approval granted. Reviewer: {reviewer_comment}"
        if approved
        else f"Human approval rejected. Reviewer: {reviewer_comment}"
    )

    return {
        "approved": approved,
        "human_approval_required": True,
        "status": "approved" if approved else "rejected",
        "comments": comments,
    }
