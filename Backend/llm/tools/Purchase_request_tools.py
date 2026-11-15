"""
Purchase Request Tools

These tools expose purchase request repository functions to the LLM.
The database session is created and closed inside each tool.
"""

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.repositories.purchase_request import (
    get_purchase_request_by_id,
    get_all_purchase_requests,
    create_purchase_request,
    update_purchase_request,
    delete_purchase_request,
)
from Backend.models.purchase_request import PurchaseRequest


@tool
def find_purchase_request_by_id(purchase_request_id: int) -> dict:
    """
    Retrieve a purchase request using its ID.

    Use this tool when the user asks:
    - Show purchase request 101
    - Get purchase request details
    - Find purchase request by ID
    """

    db = SessionLocal()

    try:
        purchase_request = get_purchase_request_by_id(
            db=db,
            purchase_request_id=purchase_request_id,
        )

        if not purchase_request:
            return {
                "success": False,
                "message": "Purchase request not found",
            }

        return {
            "id": purchase_request.id,
            "item_name": purchase_request.item_name,
            "item_quantity": purchase_request.item_quantity,
            "item_id": purchase_request.item_id,
            "item_cost": purchase_request.item_cost,
        }

    finally:
        db.close()


@tool
def list_all_purchase_requests() -> list[dict]:
    """
    Retrieve all purchase requests.

    Use this tool when the user asks:
    - List purchase requests
    - Show all purchase requests
    - Display purchase requests
    """

    db = SessionLocal()

    try:
        purchase_requests = get_all_purchase_requests(db=db)

        return [
            {
                "id": pr.id,
                "item_name": pr.item_name,
                "item_quantity": pr.item_quantity,
                "item_id": pr.item_id,
                "item_cost": pr.item_cost,
            }
            for pr in purchase_requests
        ]

    finally:
        db.close()


@tool
def create_new_purchase_request(
    item_name: str,
    item_quantity: int,
    item_id: int,
    item_cost: float,
    employee_id: int,
    department_id: int,
    status: str = "pending",
) -> dict:
    """
    Create a new purchase request.

    Use this tool only when the user explicitly asks
    to create a purchase request.

    Parameters:
    - item_name: name of the item
    - item_quantity: quantity requested
    - item_id: stationary item ID
    - item_cost: total cost of the request
    - employee_id: ID of the requesting employee
    - department_id: ID of the employee's department
    - status: request status (default: pending)
    """

    db = SessionLocal()

    try:
        purchase_request = PurchaseRequest(
            item_name=item_name,
            item_quantity=item_quantity,
            item_id=item_id,
            item_cost=item_cost,
            employee_id=employee_id,
            department_id=department_id,
            status=status,
        )

        created_request = create_purchase_request(
            db=db,
            purchase_request=purchase_request,
        )

        return {
            "success": True,
            "purchase_request_id": created_request.id,
            "message": "Purchase request created successfully.",
        }

    finally:
        db.close()


@tool
def update_existing_purchase_request(
    purchase_request_id: int,
    item_name: str,
    item_quantity: int,
    item_id: int,
    item_cost: float,
) -> dict:
    """
    Update an existing purchase request's item details.

    Use this tool only when the user explicitly requests
    updating a purchase request.
    """

    db = SessionLocal()

    try:
        existing = get_purchase_request_by_id(db=db, purchase_request_id=purchase_request_id)
        if not existing:
            return {"success": False, "message": "Purchase request not found"}

        existing.item_name = item_name
        existing.item_quantity = item_quantity
        existing.item_id = item_id
        existing.item_cost = item_cost
        db.commit()
        db.refresh(existing)

        return {
            "success": True,
            "purchase_request_id": existing.id,
            "message": "Purchase request updated successfully.",
        }

    finally:
        db.close()


@tool
def remove_purchase_request(
    purchase_request_id: int,
) -> dict:
    """
    Delete a purchase request.

    Use this tool only when the user explicitly requests
    deleting a purchase request.
    """

    db = SessionLocal()

    try:
        result = delete_purchase_request(
            db=db,
            purchase_request_id=purchase_request_id,
        )

        return result

    finally:
        db.close()


# Register all purchase request tools

purchase_request_tools = [
    find_purchase_request_by_id,
    list_all_purchase_requests,
    create_new_purchase_request,
    update_existing_purchase_request,
    remove_purchase_request,
]