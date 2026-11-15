from Backend.Database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    item_id = Column(Integer, ForeignKey('stationary.id'), nullable=True)
    item_name = Column(String(100), nullable=False)
    item_quantity = Column(Integer, nullable=False)
    item_cost = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    vendor_name = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return (
            f"<PurchaseOrder(employee_id={self.employee_id}, item_id={self.item_id}, "
            f"item_name={self.item_name}, item_quantity={self.item_quantity}, "
            f"item_cost={self.item_cost}, department_id={self.department_id}, status={self.status})>"
        )