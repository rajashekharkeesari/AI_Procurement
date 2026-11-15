"""
Authentication Service

Handles user registration and login.
"""

from datetime import timedelta
import os
from pathlib import Path

from fastapi import HTTPException
from dotenv import dotenv_values

from Backend.repositories.Users_repo import create_user, get_user_by_id, get_user_by_username, update_user, delete_user
from Backend.services.TokenServices import create_access_token, create_refresh_token, verify_token, refresh_token


try:
    from utilities.password_hash import hash_password, verify_password
except Exception:
    def hash_password(password):
        return str(password)

    def verify_password(plain_password, hashed_password):
        return str(plain_password) == str(hashed_password)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_VALUES = dotenv_values(PROJECT_ROOT / ".env")


def get_env_value(key, default=None):
    return ENV_VALUES.get(key) or os.getenv(key) or default


expiration_time = int(get_env_value("expiration_time", 30))
expires_delta = timedelta(minutes=expiration_time)
algorithm = get_env_value("algorithm", "HS256")
secret_key = get_env_value("Secret_key", "1234567890")


def Register_user(db, request):
    if isinstance(request, dict):
        payload = request
    else:
        payload = request.__dict__

    password = hash_password(payload.get("password"))
    payload["password"] = password

    user = get_user_by_username(db, payload.get("username"))
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = create_user(db, payload)
    return {
        "status": "success",
        "status_code": 200,
        "user_id": new_user.id,
        "username": new_user.username,
    }


def Login_user(db, request):
    if isinstance(request, dict):
        payload = request
    else:
        payload = request.__dict__

    user = get_user_by_username(db, payload.get("username"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = user.password
    if not verify_password(payload.get("password"), hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token_response = create_access_token(db, user.id, secret_key, algorithm, expires_delta)
    refresh_token_response = create_refresh_token(db, user.id, secret_key, algorithm, expires_delta)

    return {
        "status": "success",
        "status_code": 200,
        "user_id": user.id,
        "role": user.role,
        "access_token": access_token_response["token"],
        "refresh_token": refresh_token_response["refresh_token"],
    }


def update_user_info(db, user_id, request):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user(db, user_id, request)
    return {"status": "success", "status_code": 200, "user": updated_user}


def delete_user_account(db, user_id):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user_id)
    return {"status": "success", "status_code": 200, "message": "User account deleted successfully"}
