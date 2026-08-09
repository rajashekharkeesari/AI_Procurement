import http
from Backend.models.Employees import Employees

'''
this module contains functions to manage employees and provides access to employee data.

'''

def get_employee_by_id(db, employee_id: int) -> dict:
    """
    Retrieve an employee by their ID.

    Args:
        employee_id (int): The ID of the employee to retrieve.
        db: The database session.

    Returns:
        dict: A dictionary containing the employee's details, or None if not found.
    """
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee:
        return {
            "id": employee.id,
            "name": employee.name,
            "department_id": employee.department_id
        }
    return http.HTTPException(status_code=404, detail="Employee not found")

def get_all_employees(db) -> list:
    """
    Retrieve all employees.

    Args:
        db: The database session.

    Returns:
        list: A list of dictionaries, each containing an employee's details.
    """
    employees = db.query(Employees).all()
    return [
        {
            "id": employee.id,
            "name": employee.name,
            "department_id": employee.department_id
        }
        for employee in employees
    ]

def get_employee_department_id(db, employee_id):
    """
    Retrieve the department ID of an employee by their ID.

    Args:
        db: The database session.
        employee_id (int): The ID of the employee.

    Returns:
        int: The department ID of the employee, or None if not found.
    """
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee:
        return employee.department_id
    return http.HTTPException(status_code=404, detail="Employee not found") 


def get_employee_name(db, employee_id):
    """
    Retrieve the name of an employee by their ID.

    Args:
        db: The database session.
        employee_id (int): The ID of the employee.

    Returns:
        str: The name of the employee, or None if not found.
    """
    employee = db.query(Employees).filter(Employees.id == employee_id).first()
    if employee:
        return employee.name
    return http.HTTPException(status_code=404, detail="Employee not found")

