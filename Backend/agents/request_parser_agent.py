"""
Request Parser Agent

Parses the incoming procurement request.
Resolves employee name to employee_id and department_id
by querying the database directly, so downstream agents
have concrete IDs and don't need to guess.
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm
from Backend.Database import SessionLocal
from Backend.repositories.Employees import get_employee_by_name, get_all_employees


SYSTEM_PROMPT = """You are the Request Parser Agent in a procurement workflow.
Your job is to confirm the procurement request details are valid.

You are given already-resolved data including employee_id and department_id.
Just confirm the request looks valid and provide a brief summary.

Do NOT call any tools. Just analyze and summarize what you see."""


def request_parser_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Parse and validate the procurement request.
    Resolves employee name to IDs via direct DB lookup.
    """
    employee_name = state.get("employee", "")
    quantity = state.get("quantity", 0)
    price = state.get("price", 0.0)
    total_cost = quantity * price

    # Resolve employee by name from DB
    employee_id = None
    department_id = None

    db = SessionLocal()
    try:
        if employee_name:
            emp = get_employee_by_name(db, employee_name)
            if emp:
                employee_id = emp["id"]
                department_id = emp["department_id"]
    finally:
        db.close()

    # Use LLM just to summarize/validate
    llm = create_llm()

    user_content = (
        f"Validate this procurement request:\n"
        f"Employee: {employee_name} (ID: {employee_id}, Department ID: {department_id})\n"
        f"Item: {state.get('item', 'unknown')}\n"
        f"Quantity: {quantity}\n"
        f"Unit Price: ${price:.2f}\n"
        f"Total Cost: ${total_cost:.2f}\n"
        f"Vendor: {state.get('vendor', 'none')}\n\n"
        f"Confirm this request is valid and provide a brief summary."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    return {
        "employee": employee_name,
        "employee_id": employee_id,
        "department_id": department_id,
        "item": state.get("item", ""),
        "quantity": quantity,
        "price": price,
        "total_cost": total_cost,
        "vendor": state.get("vendor", ""),
        "approved": False,
        "status": "pending",
        "comments": f"Request parsed. {response.content}",
    }
