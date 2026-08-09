from sqlalchemy import Column, Integer, String, Float
from Backend.Database import Base

class Stationary(Base):
    __tablename__ = 'stationary'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    cost = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Stationary(name={self.name}, cost={self.cost}, quantity={self.quantity})>"