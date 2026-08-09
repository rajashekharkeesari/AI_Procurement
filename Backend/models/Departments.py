from Backend.Database import Base
from sqlalchemy import Column, Integer, String, Float

class Departments(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    budget = Column(Float, nullable=False)
    policy_limit = Column(Float, nullable=False)
    allowed_quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Department(name={self.name}, budget={self.budget}, policy_limit={self.policy_limit}, allowed_quantity={self.allowed_quantity})>"