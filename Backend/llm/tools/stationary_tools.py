"""
Stationary Item Tools

These tools expose stationary-related repository functions to the LLM.
Each tool creates and closes its own database session.
"""

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.models.stationary import Stationary
from Backend.repositories.stationary import (
    get_stationary_by_id,
    get_all_stationary,
    create_stationary,
    update_stationary,
    delete_stationary,
)


def stationary_to_dict(stationary: Stationary) -> dict:
    """Convert a Stationary database object into a dictionary."""

    return {
        "id": stationary.id,
        "name": stationary.name,
        "quantity": stationary.quantity,
        "cost": float(stationary.cost),
    }


@tool
def find_stationary_by_id(stationary_id: int) -> dict:
    """
    Retrieve a stationary item using its ID.

    Use this tool when the user asks for:
    - stationary item details
    - stationary item name, quantity, or cost
    - an item using its stationary ID
    """

    db = SessionLocal()

    try:
        stationary = get_stationary_by_id(
            db=db,
            stationary_id=stationary_id,
        )

        if stationary is None:
            return {
                "success": False,
                "message": "Stationary item not found",
            }

        return {
            "success": True,
            "stationary": stationary_to_dict(stationary),
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to retrieve stationary item: {error}",
        }

    finally:
        db.close()


@tool
def list_all_stationary_items() -> dict:
    """
    Retrieve all stationary items.

    Use this tool when the user asks to:
    - list all stationary items
    - display available stationary items
    - view stationary inventory
    """

    db = SessionLocal()

    try:
        stationary_items = get_all_stationary(db=db)

        return {
            "success": True,
            "count": len(stationary_items),
            "stationary_items": [
                stationary_to_dict(item)
                for item in stationary_items
            ],
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to retrieve stationary items: {error}",
        }

    finally:
        db.close()


@tool
def create_new_stationary_item(
    name: str,
    quantity: int,
    cost: float,
) -> dict:
    """
    Create a new stationary item.

    Use this tool only when the user clearly asks to add
    or create a new stationary item.

    The quantity must be zero or greater.
    The cost must be zero or greater.
    """

    if quantity < 0:
        return {
            "success": False,
            "message": "Quantity cannot be negative",
        }

    if cost < 0:
        return {
            "success": False,
            "message": "Cost cannot be negative",
        }

    db = SessionLocal()

    try:
        stationary = Stationary(
            name=name,
            quantity=quantity,
            cost=cost,
        )

        created_stationary = create_stationary(
            db=db,
            stationary=stationary,
        )

        return {
            "success": True,
            "message": "Stationary item created successfully",
            "stationary": stationary_to_dict(created_stationary),
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to create stationary item: {error}",
        }

    finally:
        db.close()


@tool
def update_existing_stationary_item(
    stationary_id: int,
    name: str,
    quantity: int,
    cost: float,
) -> dict:
    """
    Update an existing stationary item's name, quantity, and cost.

    Use this tool only when the user clearly asks to update
    or modify an existing stationary item.
    """

    if quantity < 0:
        return {
            "success": False,
            "message": "Quantity cannot be negative",
        }

    if cost < 0:
        return {
            "success": False,
            "message": "Cost cannot be negative",
        }

    db = SessionLocal()

    try:
        existing_stationary = get_stationary_by_id(
            db=db,
            stationary_id=stationary_id,
        )

        if existing_stationary is None:
            return {
                "success": False,
                "message": "Stationary item not found",
            }

        updated_stationary = Stationary(
            name=name,
            quantity=quantity,
            cost=cost,
        )

        stationary = update_stationary(
            db=db,
            stationary_id=stationary_id,
            updated_stationary=updated_stationary,
        )

        return {
            "success": True,
            "message": "Stationary item updated successfully",
            "stationary": stationary_to_dict(stationary),
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to update stationary item: {error}",
        }

    finally:
        db.close()


@tool
def remove_stationary_item(stationary_id: int) -> dict:
    """
    Delete a stationary item using its ID.

    Use this tool only when the user clearly asks to delete
    or remove a stationary item.
    """

    db = SessionLocal()

    try:
        stationary = get_stationary_by_id(
            db=db,
            stationary_id=stationary_id,
        )

        if stationary is None:
            return {
                "success": False,
                "message": "Stationary item not found",
            }

        delete_stationary(
            db=db,
            stationary_id=stationary_id,
        )

        return {
            "success": True,
            "stationary_id": stationary_id,
            "message": "Stationary item deleted successfully",
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to delete stationary item: {error}",
        }

    finally:
        db.close()


stationary_tools = [
    find_stationary_by_id,
    list_all_stationary_items,
    create_new_stationary_item,
    update_existing_stationary_item,
    remove_stationary_item,
]