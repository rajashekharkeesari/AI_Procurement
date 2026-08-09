from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import dotenv

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from Backend.models.Users import Users  # noqa: F401
    Base.metadata.create_all(bind=engine)


init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

