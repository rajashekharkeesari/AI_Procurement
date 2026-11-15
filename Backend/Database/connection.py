from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import dotenv

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Import all models so their tables are registered, then create them."""
    from Backend.models.Users import Users  # noqa: F401
    from Backend.models.Employees import Employees  # noqa: F401
    from Backend.models.Departments import Departments  # noqa: F401
    from Backend.models.stationary import Stationary  # noqa: F401
    from Backend.models.vendors import Vendors  # noqa: F401
    from Backend.models.purchase_request import PurchaseRequest  # noqa: F401
    from Backend.models.purchase_order import PurchaseOrder  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
