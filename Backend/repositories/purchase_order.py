import http
from Backend.models.purchase_order import PurchaseOrder
'''
this module about purchase orders, it provides functions to manage purchase orders in the database. It includes functionality to retrieve, create, update, and delete purchase orders.

'''

def get_purchase_order_by_id(db, purchase_order_id):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()

def get_all_purchase_orders(db):
    return db.query(PurchaseOrder).all()

def create_purchase_order(db, purchase_order):
    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)
    return purchase_order

def update_purchase_order(db, purchase_order_id, updated_purchase_order):
    purchase_order = get_purchase_order_by_id(db, purchase_order_id)
    try:
        if purchase_order:
            purchase_order.item_name = updated_purchase_order.item_name
            purchase_order.item_quantity = updated_purchase_order.item_quantity
            purchase_order.item_id = updated_purchase_order.item_id
            purchase_order.item_cost = updated_purchase_order.item_cost
            db.commit()
            db.refresh(purchase_order)
            return purchase_order
        else:
            return http.HTTPException(status_code=404, detail="Purchase order not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Purchase order not found")

def delete_purchase_order(db, purchase_order_id):
    purchase_order = get_purchase_order_by_id(db, purchase_order_id)
    try:
        if purchase_order:
            db.delete(purchase_order)
            db.commit()
            return {"message": "Purchase order deleted successfully"}
        else:
            return http.HTTPException(status_code=404, detail="Purchase order not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Purchase order not found")