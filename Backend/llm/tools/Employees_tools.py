"""
Employee Tools for LangChain

These tools expose employee-related repository functions to the LLM.
The LLM never receives the database session; each tool creates and
closes its own database session.
"""

from langchain.tools import tool

from Backend.Database import SessionLocal
from Backend.repositories.Employees import (
    get_employee_by_id,
    get_employee_by_name,
    get_all_employees,
    get_employee_department_id,
    get_employee_name,
)


@tool
def find_employee_by_id(employee_id: int) -> dict:
    """
    Retrieve an employee's complete details using their numeric employee ID.

    Use this tool ONLY when you have a numeric employee ID (e.g. 1, 2, 3).
    Do NOT use this tool if you only have a name string.
    """

    db = SessionLocal()

    try:
        result = get_employee_by_id(db=db, employee_id=employee_id)
        return result or {"error": "Employee not found"}
    finally:
        db.close()


@tool
def find_employee_by_name(employee_name: str) -> dict:
    """
    Find an employee by their name (supports partial matching).

    Use this tool when you have the employee's NAME (e.g. "Alice", "Bob Smith")
    and need to find their ID, department, or other details.

    This is the preferred tool when the input is a name string, not a numeric ID.
    """

    db = SessionLocal()

    try:
        result = get_employee_by_name(db=db, employee_name=employee_name)
        return result or {"error": f"No employee found matching '{employee_name}'"}
    finally:
        db.close()


@tool
def list_all_employees() -> list[dict]:
    """
    Retrieve all employees.

    Use this tool when you need to see all employees or search through them.
    """

    db = SessionLocal()

    try:
        return get_all_employees(db=db)
    finally:
        db.close()


@tool
def find_employee_department(employee_id: int) -> dict:
    """
    Retrieve the department ID of an employee using their numeric employee ID.

    Use this tool ONLY when you already have the numeric employee ID.
    If you only have a name, use find_employee_by_name first.
    """

    db = SessionLocal()

    try:
        department_id = get_employee_department_id(db=db, employee_id=employee_id)
        if department_id is None:
            return {"error": "Employee not found"}
        return {
            "employee_id": employee_id,
            "department_id": department_id,
        }
    finally:
        db.close()


@tool
def find_employee_name(employee_id: int) -> dict:
    """
    Retrieve an employee's name using their numeric employee ID.

    Use this tool ONLY when you have a numeric employee ID.
    """

    db = SessionLocal()

    try:
        employee_name = get_employee_name(db=db, employee_id=employee_id)
        if employee_name is None:
            return {"error": "Employee not found"}
        return {
            "employee_id": employee_id,
            "employee_name": employee_name,
        }
    finally:
        db.close()


# List of all employee tools
employee_tools = [
    find_employee_by_id,
    find_employee_by_name,
    list_all_employees,
    find_employee_department,
    find_employee_name,
]
