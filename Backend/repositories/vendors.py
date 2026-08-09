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
            return http.HTTPException(status_code=404, detail="Vendor not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Vendor not found") 