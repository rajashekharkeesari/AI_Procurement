"""
Vendor Tools

These tools expose vendor-related repository functions to the LLM.
Each tool creates and closes its own database session.
"""

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.models.vendors import Vendors
from Backend.repositories.vendors import (
    get_vendor_by_id,
    get_all_vendors,
    create_vendor,
    update_vendor,
    delete_vendor,
)


def vendor_to_dict(vendor: Vendors) -> dict:
    """Convert a Vendor database object into a dictionary."""

    return {
        "id": vendor.id,
        "name": vendor.name,
        "contact_info": vendor.contact_info,
        "stationary_id": vendor.stationary_id,
    }


@tool
def find_vendor_by_id(vendor_id: int) -> dict:
    """
    Retrieve a vendor using its vendor ID.

    Use this tool when the user asks for:
    - vendor details
    - vendor name
    - vendor contact information
    """

    db = SessionLocal()

    try:
        vendor = get_vendor_by_id(
            db=db,
            vendor_id=vendor_id,
        )

        if vendor is None:
            return {
                "success": False,
                "message": "Vendor not found",
            }

        return {
            "success": True,
            "vendor": vendor_to_dict(vendor),
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to retrieve vendor: {error}",
        }

    finally:
        db.close()


@tool
def list_all_vendors() -> dict:
    """
    Retrieve all vendors.

    Use this tool when the user asks to:
    - list all vendors
    - show available vendors
    - display vendor information
    """

    db = SessionLocal()

    try:
        vendors = get_all_vendors(db=db)

        return {
            "success": True,
            "count": len(vendors),
            "vendors": [
                vendor_to_dict(vendor)
                for vendor in vendors
            ],
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Failed to retrieve vendors: {error}",
        }

    finally:
        db.close()


@tool
def create_new_vendor(
    name: str,
    contact_info: str,
    stationary_id: int,
) -> dict:
    """
    Create a new vendor.

    Use this tool only when the user clearly asks
    to add or create a vendor.

    Parameters:
    - name: vendor name
    - contact_info: vendor contact information
    - stationary_id: the stationary item ID this vendor supplies
    """

    if not name.strip():
        return {
            "success": False,
            "message": "Vendor name cannot be empty",
        }

    if not contact_info.strip():
        return {
            "success": False,
            "message": "Vendor contact information cannot be empty",
        }

    db = SessionLocal()

    try:
        vendor = Vendors(
            name=name.strip(),
            contact_info=contact_info.strip(),
            stationary_id=stationary_id,
        )

        created_vendor = create_vendor(
            db=db,
            vendor=vendor,
        )

        return {
            "success": True,
            "message": "Vendor created successfully",
            "vendor": vendor_to_dict(created_vendor),
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to create vendor: {error}",
        }

    finally:
        db.close()


@tool
def update_existing_vendor(
    vendor_id: int,
    name: str,
    contact_info: str,
) -> dict:
    """
    Update an existing vendor's name and contact information.

    Use this tool only when the user clearly asks
    to update or modify a vendor.
    """

    if not name.strip():
        return {
            "success": False,
            "message": "Vendor name cannot be empty",
        }

    if not contact_info.strip():
        return {
            "success": False,
            "message": "Vendor contact information cannot be empty",
        }

    db = SessionLocal()

    try:
        existing_vendor = get_vendor_by_id(
            db=db,
            vendor_id=vendor_id,
        )

        if existing_vendor is None:
            return {
                "success": False,
                "message": "Vendor not found",
            }

        existing_vendor.name = name.strip()
        existing_vendor.contact_info = contact_info.strip()
        db.commit()
        db.refresh(existing_vendor)

        return {
            "success": True,
            "message": "Vendor updated successfully",
            "vendor": vendor_to_dict(existing_vendor),
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to update vendor: {error}",
        }

    finally:
        db.close()


@tool
def remove_vendor(vendor_id: int) -> dict:
    """
    Delete a vendor using its vendor ID.

    Use this tool only when the user clearly asks
    to delete or remove a vendor.
    """

    db = SessionLocal()

    try:
        vendor = get_vendor_by_id(
            db=db,
            vendor_id=vendor_id,
        )

        if vendor is None:
            return {
                "success": False,
                "message": "Vendor not found",
            }

        delete_vendor(
            db=db,
            vendor_id=vendor_id,
        )

        return {
            "success": True,
            "vendor_id": vendor_id,
            "message": "Vendor deleted successfully",
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "message": f"Failed to delete vendor: {error}",
        }

    finally:
        db.close()


vendor_tools = [
    find_vendor_by_id,
    list_all_vendors,
    create_new_vendor,
    update_existing_vendor,
    remove_vendor,
]