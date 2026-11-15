"""
Budget Verification Agent

Verifies whether the procurement request fits within
the department's available budget. Uses the resolved
department_id from the parser agent.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm
from Backend.Database import SessionLocal
from Backend.repositories.Department import get_department_by_id


SYSTEM_PROMPT = """You are the Budget Verification Agent in a procurement workflow.
You are given the department budget information and order cost.
Determine if the order fits within the budget.

Respond with APPROVED if total cost <= department budget, or REJECTED if it exceeds.
Include the numbers in your response.

Do NOT call any tools. Just analyze the data provided."""


def Budget_verification_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Verify budget using resolved department_id.
    """
    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))
    department_id = state.get("department_id")

    # Look up budget directly
    budget = None
    dept_name = "Unknown"

    if department_id:
        db = SessionLocal()
        try:
            dept = get_department_by_id(db, department_id)
            if dept:
                budget = float(dept.budget)
                dept_name = dept.name
        finally:
            db.close()

    # Determine budget sufficiency
    if budget is not None:
        budget_ok = total_cost <= budget
    else:
        budget_ok = False

    # Use LLM to produce a human-readable explanation
    llm = create_llm()

    user_content = (
        f"Budget verification for procurement request:\n"
        f"Department: {dept_name} (ID: {department_id})\n"
        f"Department Budget: ${budget if budget else 'UNKNOWN'}\n"
        f"Order Total Cost: ${total_cost:.2f}\n"
        f"Result: {'APPROVED - within budget' if budget_ok else 'REJECTED - exceeds budget or department not found'}\n\n"
        f"Provide a brief explanation of this budget check result."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    comments = (
        f"Budget verification passed: ${total_cost:.2f} within ${budget} budget. {response.content}"
        if budget_ok
        else f"Budget verification failed: ${total_cost:.2f} exceeds budget. {response.content}"
    )

    return {
        "budget_sufficient": budget_ok,
        "approved": budget_ok,
        "comments": comments,
    }
