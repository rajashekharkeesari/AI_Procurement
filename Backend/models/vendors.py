from Backend.Database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class Vendors(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(200), nullable=False)
    stationary_id = Column(Integer, ForeignKey('stationary.id'), nullable=False)
    price = Column(Float, nullable=True)  # Vendor-specific price for the item

    def __repr__(self):
        return f"<Vendor(name={self.name}, price={self.price})>"