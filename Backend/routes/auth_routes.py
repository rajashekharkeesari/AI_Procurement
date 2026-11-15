"""Auth routes for user registration and login."""

from Backend.Database import get_db
from Backend.services.Authentication import Register_user, Login_user
from fastapi import APIRouter, Depends

authrouter = APIRouter()


@authrouter.post("/register")
def register_user(user_data: dict, db=Depends(get_db)):
    return Register_user(db, user_data)


@authrouter.post("/login")
def login_user(user_data: dict, db=Depends(get_db)):
    return Login_user(db, user_data)


# Export the router under the expected name
router = authrouter
