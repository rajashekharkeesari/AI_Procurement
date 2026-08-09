import http
from Backend.models.purchase_request import PurchaseRequest

'''
this module contains functions to manage purchase requests. It provides functionality to retrieve, create, update, and delete purchase requests in the database.

'''

def get_purchase_request_by_id(db, purchase_request_id):
    return db.query(PurchaseRequest).filter(PurchaseRequest.id == purchase_request_id).first()

def get_all_purchase_requests(db):
    return db.query(PurchaseRequest).all()

def create_purchase_request(db, purchase_request):
    db.add(purchase_request)
    db.commit()
    db.refresh(purchase_request)
    return purchase_request

def update_purchase_request(db, purchase_request_id, updated_purchase_request):
    purchase_request = get_purchase_request_by_id(db, purchase_request_id)
    try:
        if purchase_request:
            purchase_request.item_name = updated_purchase_request.item_name
            purchase_request.item_quantity = updated_purchase_request.item_quantity
            purchase_request.item_id = updated_purchase_request.item_id
            purchase_request.item_cost = updated_purchase_request.item_cost
            db.commit()
            db.refresh(purchase_request)
            return purchase_request
        else:
            return http.HTTPException(status_code=404, detail="Purchase request not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Purchase request not found")

def delete_purchase_request(db, purchase_request_id):
    purchase_request = get_purchase_request_by_id(db, purchase_request_id)
    try:
        if purchase_request:
            db.delete(purchase_request)
            db.commit()
            return {"message": "Purchase request deleted successfully"}
        else:
            return http.HTTPException(status_code=404, detail="Purchase request not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Purchase request not found")

