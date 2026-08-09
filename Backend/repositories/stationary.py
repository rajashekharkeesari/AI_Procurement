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
            return http.HTTPException(status_code=404, detail="Stationary item not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Stationary item not found")

