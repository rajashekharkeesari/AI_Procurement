from Backend.Database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    def __repr__(self):
        return f"<Employee(name={self.name})>"