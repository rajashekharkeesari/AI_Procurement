"""
Data Routes

Read-only API endpoints to serve entity data
(employees, departments, vendors, stationary) to the frontend.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Backend.Database import get_db
from Backend.models.Employees import Employees
from Backend.models.Departments import Departments
from Backend.models.vendors import Vendors
from Backend.models.stationary import Stationary

router = APIRouter()


@router.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    employees = db.query(Employees).all()
    return [
        {"id": e.id, "name": e.name, "department_id": e.department_id}
        for e in employees
    ]


@router.post("/employees")
def create_employee(payload: dict, db: Session = Depends(get_db)):
    employee = Employees(
        name=payload["name"],
        department_id=payload["department_id"],
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return {"id": employee.id, "name": employee.name, "department_id": employee.department_id}


@router.get("/departments")
def list_departments(db: Session = Depends(get_db)):
    departments = db.query(Departments).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "budget": float(d.budget),
            "policy_limit": float(d.policy_limit),
        }
        for d in departments
    ]


@router.post("/departments")
def create_department(payload: dict, db: Session = Depends(get_db)):
    dept = Departments(
        name=payload["name"],
        budget=payload["budget"],
        policy_limit=payload["policy_limit"],
        allowed_quantity=payload.get("allowed_quantity", 100),
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return {"id": dept.id, "name": dept.name, "budget": float(dept.budget), "policy_limit": float(dept.policy_limit)}


@router.get("/vendors")
def list_vendors(db: Session = Depends(get_db)):
    vendors = db.query(Vendors).all()
    return [
        {
            "id": v.id,
            "name": v.name,
            "contact_info": v.contact_info,
            "stationary_id": v.stationary_id,
            "price": float(v.price) if v.price else None,
        }
        for v in vendors
    ]


@router.post("/vendors")
def create_vendor_endpoint(payload: dict, db: Session = Depends(get_db)):
    vendor = Vendors(
        name=payload["name"],
        contact_info=payload["contact_info"],
        stationary_id=payload["stationary_id"],
        price=payload.get("price"),
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return {"id": vendor.id, "name": vendor.name, "contact_info": vendor.contact_info, "stationary_id": vendor.stationary_id, "price": float(vendor.price) if vendor.price else None}


@router.get("/stationary")
def list_stationary(db: Session = Depends(get_db)):
    items = db.query(Stationary).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "cost": float(s.cost),
            "quantity": s.quantity,
        }
        for s in items
    ]


@router.post("/stationary")
def create_stationary_endpoint(payload: dict, db: Session = Depends(get_db)):
    item = Stationary(
        name=payload["name"],
        cost=payload["cost"],
        quantity=payload["quantity"],
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "cost": float(item.cost), "quantity": item.quantity}


@router.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    from Backend.models.purchase_order import PurchaseOrder
    orders = db.query(PurchaseOrder).all()
    return [
        {
            "id": o.id,
            "item_name": o.item_name,
            "item_quantity": o.item_quantity,
            "item_cost": float(o.item_cost),
            "status": o.status,
            "vendor_name": o.vendor_name or "—",
            "employee_id": o.employee_id,
            "department_id": o.department_id,
        }
        for o in orders
    ]


@router.get("/requests")
def list_requests(db: Session = Depends(get_db)):
    from Backend.models.purchase_request import PurchaseRequest
    requests = db.query(PurchaseRequest).all()
    return [
        {
            "id": r.id,
            "item_name": r.item_name,
            "item_quantity": r.item_quantity,
            "item_cost": float(r.item_cost),
            "status": r.status,
            "employee_id": r.employee_id,
            "department_id": r.department_id,
        }
        for r in requests
    ]


# --- UPDATE endpoints ---

@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, payload: dict, db: Session = Depends(get_db)):
    emp = db.query(Employees).filter(Employees.id == employee_id).first()
    if not emp:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Employee not found")
    if "name" in payload:
        emp.name = payload["name"]
    if "department_id" in payload:
        emp.department_id = payload["department_id"]
    db.commit()
    db.refresh(emp)
    return {"id": emp.id, "name": emp.name, "department_id": emp.department_id}


@router.put("/vendors/{vendor_id}")
def update_vendor_endpoint(vendor_id: int, payload: dict, db: Session = Depends(get_db)):
    vendor = db.query(Vendors).filter(Vendors.id == vendor_id).first()
    if not vendor:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Vendor not found")
    if "name" in payload:
        vendor.name = payload["name"]
    if "contact_info" in payload:
        vendor.contact_info = payload["contact_info"]
    if "stationary_id" in payload:
        vendor.stationary_id = payload["stationary_id"]
    if "price" in payload:
        vendor.price = payload["price"]
    db.commit()
    db.refresh(vendor)
    return {"id": vendor.id, "name": vendor.name, "contact_info": vendor.contact_info, "stationary_id": vendor.stationary_id, "price": float(vendor.price) if vendor.price else None}


@router.put("/stationary/{stationary_id}")
def update_stationary_endpoint(stationary_id: int, payload: dict, db: Session = Depends(get_db)):
    item = db.query(Stationary).filter(Stationary.id == stationary_id).first()
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Stationary item not found")
    if "name" in payload:
        item.name = payload["name"]
    if "cost" in payload:
        item.cost = payload["cost"]
    if "quantity" in payload:
        item.quantity = payload["quantity"]
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "cost": float(item.cost), "quantity": item.quantity}


@router.put("/departments/{department_id}")
def update_department_endpoint(department_id: int, payload: dict, db: Session = Depends(get_db)):
    dept = db.query(Departments).filter(Departments.id == department_id).first()
    if not dept:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Department not found")
    if "name" in payload:
        dept.name = payload["name"]
    if "budget" in payload:
        dept.budget = payload["budget"]
    if "policy_limit" in payload:
        dept.policy_limit = payload["policy_limit"]
    db.commit()
    db.refresh(dept)
    return {"id": dept.id, "name": dept.name, "budget": float(dept.budget), "policy_limit": float(dept.policy_limit)}
