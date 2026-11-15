"""
Purchase Order Agent

Creates or rejects the purchase order. On approval:
- Creates the purchase order in DB
- Deducts stock from stationary
- Deducts cost from department budget
"""

from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from Backend.graph.state import GraphState
from Backend.llm.llm import create_llm
from Backend.Database import SessionLocal
from Backend.models.purchase_order import PurchaseOrder
from Backend.repositories.stationary import get_stationary_by_name, deduct_stationary_stock
from Backend.repositories.Department import get_department_by_id, change_department_budget_on_order


SYSTEM_PROMPT = """You are the Purchase Order Agent in a procurement workflow.
You are given the final decision and order details.
Summarize what happened — whether the order was placed or rejected and why.

Do NOT call any tools."""


def purchase_order_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Create purchase order in DB if approved, deducting stock and budget.
    """
    approved = state.get("approved", False)
    total_cost = state.get("total_cost", state.get("quantity", 0) * state.get("price", 0.0))
    quantity = state.get("quantity", 0)
    item_name = state.get("item", "")
    department_id = state.get("department_id")
    employee_id = state.get("employee_id")

    purchase_order_id = None
    order_details = ""

    if approved:
        db = SessionLocal()
        try:
            # Find the stationary item to get its ID
            item_record = get_stationary_by_name(db, item_name)
            item_id = item_record["id"] if item_record else None

            # Deduct stock if item found
            if item_id:
                stock_result = deduct_stationary_stock(db, item_id, quantity)
                if stock_result and stock_result.get("error"):
                    # Insufficient stock — reject
                    return {
                        "status": "rejected",
                        "approved": False,
                        "comments": f"Order rejected: {stock_result['error']}. Available: {stock_result.get('available', 0)}",
                    }

            # Deduct budget from department
            if department_id:
                change_department_budget_on_order(db, department_id, total_cost)

            # Create the purchase order
            po = PurchaseOrder(
                item_name=item_name,
                item_quantity=quantity,
                item_id=item_id,
                item_cost=total_cost,
                employee_id=employee_id,
                department_id=department_id,
                vendor_name=state.get("vendor", ""),
                status="ordered",
            )
            db.add(po)
            db.commit()
            db.refresh(po)
            purchase_order_id = po.id

            order_details = f"Order #{po.id} created. Stock deducted. Budget updated."

        except Exception as e:
            db.rollback()
            order_details = f"Error creating order: {str(e)}"
            return {
                "status": "rejected",
                "comments": f"Purchase order failed: {order_details}",
            }
        finally:
            db.close()

    # LLM summary
    llm = create_llm()

    user_content = (
        f"Purchase order result:\n"
        f"Approved: {approved}\n"
        f"Item: {item_name}\n"
        f"Quantity: {quantity}\n"
        f"Total Cost: ${total_cost:.2f}\n"
        f"Order Details: {order_details if approved else 'Order rejected - not approved'}\n"
        f"Provide a brief confirmation or rejection message."
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)

    if approved:
        return {
            "status": "ordered",
            "purchase_order_id": purchase_order_id,
            "comments": f"Purchase order #{purchase_order_id} created. {response.content}",
        }
    else:
        return {
            "status": "rejected",
            "comments": f"Purchase order rejected. {response.content}",
        }
