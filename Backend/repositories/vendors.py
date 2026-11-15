import http
from Backend.models.vendors import Vendors

'''
this module about vendors, it provides functions to manage vendors in the database. It includes functionality to retrieve, create, update, and delete vendors.

'''

def get_vendor_by_id(db, vendor_id):
    return db.query(Vendors).filter(Vendors.id == vendor_id).first()

def get_all_vendors(db):
    return db.query(Vendors).all()

def create_vendor(db, vendor):
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor

def update_vendor(db, vendor_id, updated_vendor):
    vendor = get_vendor_by_id(db, vendor_id)
    try:
        if vendor:
            vendor.name = updated_vendor.name
            vendor.contact_info = updated_vendor.contact_info
            db.commit()
            db.refresh(vendor)
            return vendor
        else:
            return http.HTTPException(status_code=404, detail="Vendor not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Vendor not found")

def delete_vendor(db, vendor_id):
    vendor = get_vendor_by_id(db, vendor_id)
    try:
        if vendor:
            db.delete(vendor)
            db.commit()
            return {"message": "Vendor deleted successfully"}
        else:
            return None
    except Exception as e:
        db.rollback()
        raise e


def get_vendors_by_stationary_id(db, stationary_id):
    """Get all vendors that supply a specific stationary item."""
    return db.query(Vendors).filter(Vendors.stationary_id == stationary_id).all()


def get_cheapest_vendor_for_item(db, stationary_id):
    """
    Find the cheapest vendor for a given stationary item.
    If vendors have prices, pick the lowest. Otherwise pick the first one.
    """
    vendors = db.query(Vendors).filter(
        Vendors.stationary_id == stationary_id
    ).all()

    if not vendors:
        return None

    # Filter vendors that have a price set
    priced_vendors = [v for v in vendors if v.price is not None]

    if priced_vendors:
        # Return the one with lowest price
        cheapest = min(priced_vendors, key=lambda v: v.price)
        return {
            "id": cheapest.id,
            "name": cheapest.name,
            "contact_info": cheapest.contact_info,
            "price": float(cheapest.price),
            "all_vendors": [
                {"id": v.id, "name": v.name, "price": float(v.price) if v.price else None}
                for v in vendors
            ],
        }
    else:
        # No prices set — return first vendor
        first = vendors[0]
        return {
            "id": first.id,
            "name": first.name,
            "contact_info": first.contact_info,
            "price": None,
            "all_vendors": [
                {"id": v.id, "name": v.name, "price": None}
                for v in vendors
            ],
        } 