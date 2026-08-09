from Backend.Database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class Vendors(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(200), nullable=False)
    stationary_id = Column(Integer, ForeignKey('stationary.id'), nullable=False)

    def __repr__(self):
        return f"<Vendor(name={self.name}, contact_info={self.contact_info})>"