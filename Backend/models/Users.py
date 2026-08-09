from Backend.Database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    employee_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"