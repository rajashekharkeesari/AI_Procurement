"""
Purchase Order Tools

These tools expose purchase order repository functions to the LLM.
The database session is created and closed inside each tool.
"""

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.repositories.purchase_order import (
    get_purchase_order_by_id,
    get_all_purchase_orders,
    create_purchase_order,
    update_purchase_order,
    delete_purchase_order,
)
from Backend.models.purchase_order import PurchaseOrder


@tool
def find_purchase_order_by_id(purchase_order_id: int) -> dict:
    """
    Retrieve a purchase order using its ID.

    Use this tool when the user asks:
    - Show purchase order 101
    - Get purchase order details
    - Find purchase order by ID
    """

    db = SessionLocal()

    try:
        purchase_order = get_purchase_order_by_id(
            db=db,
            purchase_order_id=purchase_order_id,
        )

        if not purchase_order:
            return {
                "success": False,
                "message": "Purchase order not found",
            }

        return {
            "id": purchase_order.id,
            "item_name": purchase_order.item_name,
            "item_quantity": purchase_order.item_quantity,
            "item_id": purchase_order.item_id,
            "item_cost": purchase_order.item_cost,
        }

    finally:
        db.close()


@tool
def list_all_purchase_orders() -> list[dict]:
    """
    Retrieve all purchase orders.

    Use this tool when the user asks:
    - List purchase orders
    - Show all purchase orders
    - Display purchase orders
    """

    db = SessionLocal()

    try:
        purchase_orders = get_all_purchase_orders(db=db)

        return [
            {
                "id": po.id,
                "item_name": po.item_name,
                "item_quantity": po.item_quantity,
                "item_id": po.item_id,
                "item_cost": po.item_cost,
            }
            for po in purchase_orders
        ]

    finally:
        db.close()


@tool
def create_new_purchase_order(
    item_name: str,
    item_quantity: int,
    item_id: int,
    item_cost: float,
) -> dict:
    """
    Create a new purchase order.

    Use this tool only when the user explicitly asks
    to create a purchase order.
    """

    db = SessionLocal()

    try:
        purchase_order = PurchaseOrder(
            item_name=item_name,
            item_quantity=item_quantity,
            item_id=item_id,
            item_cost=item_cost,
        )

        created_order = create_purchase_order(
            db=db,
            purchase_order=purchase_order,
        )

        return {
            "success": True,
            "purchase_order_id": created_order.id,
            "message": "Purchase order created successfully.",
        }

    finally:
        db.close()


@tool
def update_existing_purchase_order(
    purchase_order_id: int,
    item_name: str,
    item_quantity: int,
    item_id: int,
    item_cost: float,
) -> dict:
    """
    Update an existing purchase order.

    Use this tool only when the user explicitly requests
    updating a purchase order.
    """

    db = SessionLocal()

    try:
        updated_purchase_order = PurchaseOrder(
            item_name=item_name,
            item_quantity=item_quantity,
            item_id=item_id,
            item_cost=item_cost,
        )

        purchase_order = update_purchase_order(
            db=db,
            purchase_order_id=purchase_order_id,
            updated_purchase_order=updated_purchase_order,
        )

        return {
            "success": True,
            "purchase_order_id": purchase_order.id,
            "message": "Purchase order updated successfully.",
        }

    finally:
        db.close()


@tool
def remove_purchase_order(purchase_order_id: int) -> dict:
    """
    Delete a purchase order.

    Use this tool only when the user explicitly requests
    deleting a purchase order.
    """

    db = SessionLocal()

    try:
        result = delete_purchase_order(
            db=db,
            purchase_order_id=purchase_order_id,
        )

        return result

    finally:
        db.close()


# Register all purchase order tools

purchase_order_tools = [
    find_purchase_order_by_id,
    list_all_purchase_orders,
    create_new_purchase_order,
    update_existing_purchase_order,
    remove_purchase_order,
]