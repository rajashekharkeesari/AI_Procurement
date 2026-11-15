"""
Token Services

Create and verify JWT tokens for authentication.
"""

from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from Backend.repositories.Users_repo import get_user_by_id


def create_access_token(db, user_id, secret_key, algorithm, expires_delta):
    """Create a JWT access token."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expire = datetime.utcnow() + expires_delta
    payload = {"user_id": user_id, "exp": expire}
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return {"status": "success", "status_code": 200, "user_id": user_id, "token": token}


def create_refresh_token(db, user_id, secret_key, algorithm, expires_delta):
    """Create a JWT refresh token (longer expiry)."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expire = datetime.utcnow() + (expires_delta * 2)
    payload = {"user_id": user_id, "exp": expire, "type": "refresh"}
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return {"status": "success", "status_code": 200, "user_id": user_id, "refresh_token": token}


def verify_token(db, token, secret_key, algorithm):
    """Verify a JWT token and return the user_id."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "status_code": 200, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def refresh_token(db, token, secret_key, algorithm, expires_delta):
    """Refresh an expired access token using a valid refresh token."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user = get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        new_access_token = create_access_token(db, user_id, secret_key, algorithm, expires_delta)
        return new_access_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
