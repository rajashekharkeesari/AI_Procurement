# tools/department_tools.py

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.repositories.Department import (
    get_department_by_id,
    get_all_departments,
    check_budget_and_policy_limit,
    update_department_budget,
    update_department_policy_limit,
    change_department_budget_on_order,
)


@tool
def get_department_details(department_id: int) -> dict:
    """
    Get the details of a department using its department ID.

    Use this tool when the user asks about a department's name,
    available budget, or policy limit.
    """

    db = SessionLocal()

    try:
        department = get_department_by_id(
            db=db,
            department_id=department_id,
        )

        return {
            "id": department.id,
            "name": department.name,
            "budget": float(department.budget),
            "policy_limit": float(department.policy_limit),
        }

    finally:
        db.close()


@tool
def list_departments() -> list[dict]:
    """
    Get all departments.

    Use this tool when the user asks to list or display
    all available departments.
    """

    db = SessionLocal()

    try:
        departments = get_all_departments(db)

        return [
            {
                "id": department.id,
                "name": department.name,
                "budget": float(department.budget),
                "policy_limit": float(department.policy_limit),
            }
            for department in departments
        ]

    finally:
        db.close()


@tool
def validate_department_order(
    department_id: int,
    item_cost: float,
    item_quantity: int,
) -> dict:
    """
    Check whether an order is allowed under a department's
    available budget and policy limit.

    Use this tool before placing or approving an order.
    """

    db = SessionLocal()

    try:
        check_budget_and_policy_limit(
            db=db,
            department_id=department_id,
            item_cost=item_cost,
            item_quantity=item_quantity,
        )

        total_cost = item_cost * item_quantity

        return {
            "allowed": True,
            "department_id": department_id,
            "item_cost": item_cost,
            "item_quantity": item_quantity,
            "total_cost": total_cost,
            "message": "Order is within the budget and policy limit.",
        }

    finally:
        db.close()


@tool
def set_department_budget(
    department_id: int,
    new_budget: float,
) -> dict:
    """
    Update the budget of a department.

    Use this tool only when the user clearly asks to change
    or update a department's budget.
    """

    db = SessionLocal()

    try:
        department = update_department_budget(
            db=db,
            department_id=department_id,
            new_budget=new_budget,
        )

        return {
            "success": True,
            "department_id": department.id,
            "department_name": department.name,
            "new_budget": float(department.budget),
        }

    finally:
        db.close()


@tool
def set_department_policy_limit(
    department_id: int,
    new_policy_limit: float,
) -> dict:
    """
    Update the policy limit of a department.

    Use this tool only when the user clearly asks to change
    the department's policy limit.
    """

    db = SessionLocal()

    try:
        department = update_department_policy_limit(
            db=db,
            department_id=department_id,
            new_policy_limit=new_policy_limit,
        )

        return {
            "success": True,
            "department_id": department.id,
            "department_name": department.name,
            "new_policy_limit": float(department.policy_limit),
        }

    finally:
        db.close()


@tool
def deduct_order_cost_from_budget(
    department_id: int,
    order_cost: float,
) -> dict:
    """
    Deduct an approved order cost from a department's budget.

    Use this tool only after the order has been approved
    and the user clearly requests the budget deduction.
    """

    db = SessionLocal()

    try:
        department = change_department_budget_on_order(
            db=db,
            department_id=department_id,
            order_cost=order_cost,
        )

        return {
            "success": True,
            "department_id": department.id,
            "deducted_amount": order_cost,
            "remaining_budget": float(department.budget),
        }

    finally:
        db.close()

#list of tools
Department_tools = [
set_department_policy_limit,deduct_order_cost_from_budget,set_department_budget,validate_department_order,list_departments,get_department_details

]