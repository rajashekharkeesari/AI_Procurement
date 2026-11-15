"""
Database Seeder

Seeds the database with initial data for departments, employees,
stationary items, vendors, and a default admin user.

Run: python -m Backend.seed
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from Backend.Database import SessionLocal, init_db
from Backend.models.Departments import Departments
from Backend.models.Employees import Employees
from Backend.models.stationary import Stationary
from Backend.models.vendors import Vendors
from Backend.models.Users import Users
from Backend.models.purchase_request import PurchaseRequest
from Backend.models.purchase_order import PurchaseOrder


def seed():
    """Seed the database with sample data."""
    init_db()
    db = SessionLocal()

    try:
        # --- Departments ---
        departments_data = [
            {"name": "Engineering", "budget": 50000.00, "policy_limit": 10000.00, "allowed_quantity": 100},
            {"name": "Marketing", "budget": 30000.00, "policy_limit": 5000.00, "allowed_quantity": 50},
            {"name": "Finance", "budget": 40000.00, "policy_limit": 8000.00, "allowed_quantity": 75},
            {"name": "HR", "budget": 20000.00, "policy_limit": 3000.00, "allowed_quantity": 40},
            {"name": "Operations", "budget": 60000.00, "policy_limit": 15000.00, "allowed_quantity": 200},
        ]

        if db.query(Departments).count() == 0:
            for dept in departments_data:
                db.add(Departments(**dept))
            db.commit()
            print(f"  Seeded {len(departments_data)} departments")
        else:
            print("  Departments already exist, skipping")

        # --- Employees ---
        employees_data = [
            {"name": "Alice Johnson", "department_id": 1},
            {"name": "Bob Smith", "department_id": 1},
            {"name": "Carol Williams", "department_id": 2},
            {"name": "David Brown", "department_id": 3},
            {"name": "Eve Davis", "department_id": 4},
            {"name": "Frank Miller", "department_id": 5},
            {"name": "Grace Wilson", "department_id": 2},
            {"name": "Henry Taylor", "department_id": 3},
        ]

        if db.query(Employees).count() == 0:
            for emp in employees_data:
                db.add(Employees(**emp))
            db.commit()
            print(f"  Seeded {len(employees_data)} employees")
        else:
            print("  Employees already exist, skipping")

        # --- Stationary Items ---
        stationary_data = [
            {"name": "A4 Paper (500 sheets)", "cost": 5.99, "quantity": 1000},
            {"name": "Ballpoint Pen (box of 12)", "cost": 3.49, "quantity": 500},
            {"name": "Notebook (ruled, 200 pages)", "cost": 4.99, "quantity": 300},
            {"name": "Printer Toner Cartridge", "cost": 89.99, "quantity": 50},
            {"name": "Whiteboard Marker (pack of 4)", "cost": 7.99, "quantity": 200},
            {"name": "Stapler", "cost": 12.99, "quantity": 100},
            {"name": "Sticky Notes (pack of 6)", "cost": 6.49, "quantity": 400},
            {"name": "File Folder (pack of 10)", "cost": 8.99, "quantity": 250},
            {"name": "Desk Lamp", "cost": 34.99, "quantity": 30},
            {"name": "Ergonomic Mouse", "cost": 49.99, "quantity": 40},
        ]

        if db.query(Stationary).count() == 0:
            for item in stationary_data:
                db.add(Stationary(**item))
            db.commit()
            print(f"  Seeded {len(stationary_data)} stationary items")
        else:
            print("  Stationary items already exist, skipping")

        # --- Vendors ---
        vendors_data = [
            {"name": "Office Depot", "contact_info": "office.depot@example.com", "stationary_id": 1, "price": 5.49},
            {"name": "Staples Inc.", "contact_info": "sales@staples.example.com", "stationary_id": 2, "price": 3.29},
            {"name": "Amazon Business", "contact_info": "business@amazon.example.com", "stationary_id": 4, "price": 79.99},
            {"name": "Paper World", "contact_info": "info@paperworld.example.com", "stationary_id": 1, "price": 4.99},
            {"name": "Tech Supplies Co.", "contact_info": "orders@techsupplies.example.com", "stationary_id": 10, "price": 44.99},
        ]

        if db.query(Vendors).count() == 0:
            for vendor in vendors_data:
                db.add(Vendors(**vendor))
            db.commit()
            print(f"  Seeded {len(vendors_data)} vendors")
        else:
            print("  Vendors already exist, skipping")

        # --- Users (default admin and sample user) ---
        users_data = [
            {"username": "admin", "password": "admin123", "role": "admin", "employee_id": None},
            {"username": "alice", "password": "alice123", "role": "user", "employee_id": 1},
            {"username": "bob", "password": "bob123", "role": "user", "employee_id": 2},
            {"username": "carol", "password": "carol123", "role": "manager", "employee_id": 3},
            {"username": "david", "password": "david123", "role": "user", "employee_id": 4},
        ]

        if db.query(Users).count() == 0:
            for user in users_data:
                db.add(Users(**user))
            db.commit()
            print(f"  Seeded {len(users_data)} users")
        else:
            print("  Users already exist, skipping")

        print("\nDatabase seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding database...")
    seed()
