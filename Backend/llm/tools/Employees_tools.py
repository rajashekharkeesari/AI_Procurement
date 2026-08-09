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
    get_all_employees,
    get_employee_department_id,
    get_employee_name,
)


@tool
def find_employee_by_id(employee_id: int) -> dict:
    """
    Retrieve an employee's complete details using their employee ID.

    Use this tool when the user asks for:
    - employee details
    - employee information
    - employee profile
    """

    db = SessionLocal()

    try:
        return get_employee_by_id(
            db=db,
            employee_id=employee_id,
        )
    finally:
        db.close()


@tool
def list_all_employees() -> list[dict]:
    """
    Retrieve all employees.

    Use this tool when the user asks to:
    - list employees
    - show all employees
    - display employees
    """

    db = SessionLocal()

    try:
        return get_all_employees(db=db)
    finally:
        db.close()


@tool
def find_employee_department(employee_id: int) -> dict:
    """
    Retrieve the department ID of an employee.

    Use this tool when the user asks:
    - Which department does an employee belong to?
    - Employee department
    """

    db = SessionLocal()

    try:
        department_id = get_employee_department_id(
            db=db,
            employee_id=employee_id,
        )

        return {
            "employee_id": employee_id,
            "department_id": department_id,
        }
    finally:
        db.close()


@tool
def find_employee_name(employee_id: int) -> dict:
    """
    Retrieve an employee's name using their employee ID.

    Use this tool when the user asks:
    - What is the employee's name?
    - Who is employee <id>?
    """

    db = SessionLocal()

    try:
        employee_name = get_employee_name(
            db=db,
            employee_id=employee_id,
        )

        return {
            "employee_id": employee_id,
            "employee_name": employee_name,
        }
    finally:
        db.close()


# List of all employee tools
employee_tools = [
    find_employee_by_id,
    list_all_employees,
    find_employee_department,
    find_employee_name,
]