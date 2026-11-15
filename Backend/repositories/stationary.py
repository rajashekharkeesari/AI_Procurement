import http
from Backend.models.stationary import Stationary
'''
this module about stationary items, it provides functions to manage stationary items in the database. It includes functionality to retrieve, create, update, and delete stationary items.

'''

def get_stationary_by_id(db, stationary_id):
    return db.query(Stationary).filter(Stationary.id == stationary_id).first()

def get_all_stationary(db):
    return db.query(Stationary).all()

def create_stationary(db, stationary):
    db.add(stationary)
    db.commit()
    db.refresh(stationary)
    return stationary

def update_stationary(db, stationary_id, updated_stationary):
    stationary = get_stationary_by_id(db, stationary_id)
    try:
        if stationary:
            stationary.name = updated_stationary.name
            stationary.quantity = updated_stationary.quantity
            stationary.cost = updated_stationary.cost
            db.commit()
            db.refresh(stationary)
            return stationary
        else:
            return http.HTTPException(status_code=404, detail="Stationary item not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Stationary item not found")

def delete_stationary(db, stationary_id):
    stationary = get_stationary_by_id(db, stationary_id)
    try:
        if stationary:
            db.delete(stationary)
            db.commit()
            return {"message": "Stationary item deleted successfully"}
        else:
            return None
    except Exception as e:
        db.rollback()
        raise e


def deduct_stationary_stock(db, stationary_id, quantity):
    """Deduct quantity from stationary stock after an order is approved."""
    stationary = get_stationary_by_id(db, stationary_id)
    if not stationary:
        return None
    if stationary.quantity < quantity:
        return {"error": "Insufficient stock", "available": stationary.quantity}
    stationary.quantity -= quantity
    db.commit()
    db.refresh(stationary)
    return {"success": True, "remaining_stock": stationary.quantity}


def get_stationary_by_name(db, name: str):
    """Find stationary item by name (case-insensitive partial match)."""
    item = db.query(Stationary).filter(Stationary.name.ilike(f"%{name}%")).first()
    if item:
        return {"id": item.id, "name": item.name, "cost": float(item.cost), "quantity": item.quantity}
    return None

