"""
Policy Checker Agent

Checks whether a procurement request complies with
departmental policies using the resolved department_id.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm
from Backend.Database import SessionLocal
from Backend.repositories.Department import get_department_by_id


SYSTEM_PROMPT = """You are the Policy Checker Agent in a procurement workflow.
You are given department policy information and order details.
Determine if the order complies with policy limits.

Respond with COMPLIANT if total cost <= policy limit, or NON-COMPLIANT if it exceeds.

Do NOT call any tools. Just analyze the data provided."""


def policy_checker_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Check policy compliance using resolved department_id.
    """
    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))
    department_id = state.get("department_id")

    # Look up policy limit directly
    policy_limit = None
    dept_name = "Unknown"

    if department_id:
        db = SessionLocal()
        try:
            dept = get_department_by_id(db, department_id)
            if dept:
                policy_limit = float(dept.policy_limit)
                dept_name = dept.name
        finally:
            db.close()

    # Determine compliance
    if policy_limit is not None:
        compliant = total_cost <= policy_limit
    else:
        compliant = False

    # LLM explanation
    llm = create_llm()

    user_content = (
        f"Policy compliance check:\n"
        f"Department: {dept_name} (ID: {department_id})\n"
        f"Policy Limit: ${policy_limit if policy_limit else 'UNKNOWN'}\n"
        f"Order Total Cost: ${total_cost:.2f}\n"
        f"Budget Sufficient: {state.get('budget_sufficient', False)}\n"
        f"Risk Level: {state.get('risk_level', 'unknown')}\n"
        f"Result: {'COMPLIANT' if compliant else 'NON-COMPLIANT'}\n\n"
        f"Provide a brief policy compliance summary."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    comments = (
        f"Policy compliance passed. {response.content}"
        if compliant
        else f"Policy compliance failed. {response.content}"
    )

    return {
        "policy_compliant": compliant,
        "approved": compliant and state.get("budget_sufficient", False),
        "comments": comments,
    }
