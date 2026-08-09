import http
from Backend.models.Departments import Departments
'''
this file contains the repository class for the Department model. It provides methods to interact with the database for CRUD operations related to departments. 
'''

def get_department_by_id(db, department_id):
    return db.query(Departments).filter(Departments.id == department_id).first()

def get_all_departments(db):
    return db.query(Departments).all()

def create_department(db, department):
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

def update_department(db, department_id, updated_department):
    department = get_department_by_id(db, department_id)
    try:
        if department:
            department.name = updated_department.name
            department.budget = updated_department.budget
            department.policy_limit = updated_department.policy_limit
            db.commit()
            db.refresh(department)
            return department
        else:
            return http.HTTPException(status_code=404, detail="Department not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Department not found")

def delete_department(db, department_id):
    department = get_department_by_id(db, department_id)
    try:
        if department:
            db.delete(department)
            db.commit()
            return {"message": "Department deleted successfully"}
        else:
            return http.HTTPException(status_code=404, detail="Department not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="Department not found")  

def get_department_budget_and_policy_limit(db, department_id):
    department = get_department_by_id(db, department_id)
    if department:
        return department.budget, department.policy_limit
    else:
        return http.HTTPException(status_code=404, detail="Department not found")  

def check_budget_and_policy_limit(db, department_id, item_cost, item_quantity):
    department = get_department_by_id(db, department_id)
    if department:
        total_cost = item_cost * item_quantity
        if total_cost <= department.budget and total_cost <= department.policy_limit:
            return True
        else:
            return http.HTTPException(status_code=400, detail="Budget or policy limit exceeded")
    else:
        return http.HTTPException(status_code=404, detail="Department not found")

def get_department_budget(db, department_id):
    department = get_department_by_id(db, department_id)
    if department:
        return department.budget
    else:
        return http.HTTPException(status_code=404, detail="Department not found")

def get_department_policy_limit(db, department_id):
    department = get_department_by_id(db, department_id)
    if department:
        return department.policy_limit
    else:
        return http.HTTPException(status_code=404, detail="Department not found")


def update_department_budget(db, department_id, new_budget):
    department = get_department_by_id(db, department_id)
    if department:
        department.budget = new_budget
        db.commit()
        db.refresh(department)
        return department
    else:
        return http.HTTPException(status_code=404, detail="Department not found")

def update_department_policy_limit(db, department_id, new_policy_limit):
    department = get_department_by_id(db, department_id)
    if department:
        department.policy_limit = new_policy_limit
        db.commit()
        db.refresh(department)
        return department
    else:
        return http.HTTPException(status_code=404, detail="Department not found")

def get_department_budget_and_policy_limit(db, department_id):
    department = get_department_by_id(db, department_id)
    if department:
        return department.budget, department.policy_limit
    else:
        return http.HTTPException(status_code=404, detail="Department not found")

    
def change_department_budget_on_order(db, department_id, order_cost):
    department = get_department_by_id(db, department_id)
    if department:
        department.budget = department.budget - order_cost
        db.commit()
        db.refresh(department)
        return department
    else:
        return http.HTTPException(status_code=404, detail="Department not found")