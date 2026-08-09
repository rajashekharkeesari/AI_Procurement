'''
this module is used to create and manage JWT tokens for authentication and authorization purposes. It provides functions to create, retrieve, update, and delete JWT tokens in the database.
'''
from datetime import datetime, timedelta
from jose import jwt
from repositories.Users_repo import get_user_by_id

def create_access_token(db,user_id, Secret_key, algorithm, expires_delta):
    # Create a new JWT token
    user = get_user_by_id(db, user_id)
    if not user:
        return http.HTTPException(status_code=404, detail="User not found")
    token = jwt.encode({"user": user, "exp": expires_delta}, Secret_key, algorithm=algorithm)
    return { "status": "success","status_code": 200,"user_id": user_id, "token": token }


def create_refresh_token(db,user_id, Secret_key, algorithm, expires_delta):
    # Create a new JWT refresh token
    user = get_user_by_id(db, user_id)
    if not user:
        return http.HTTPException(status_code=404, detail="User not found")
    refresh_token = jwt.encode({"user": user, "exp": expires_delta}, Secret_key, algorithm=algorithm)
    return { "status": "success","status_code": 200,"user_id": user_id, "refresh_token": refresh_token }

def verify_token(db, token, Secret_key, algorithm):
    # Verify the JWT token
    try:
        payload = jwt.decode(token, Secret_key, algorithms=[algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            return http.HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_id(db, user_id)
        if user is None:
            return http.HTTPException(status_code=404, detail="User not found")
        return { "status": "success","status_code": 200,"user_id": user_id }
    except jwt.ExpiredSignatureError:
        return http.HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        return http.HTTPException(status_code=401, detail="Invalid token")

def refresh_token(db, refresh_token, Secret_key, algorithm, expires_delta):
    # Refresh the JWT token
    try:
        payload = jwt.decode(refresh_token, Secret_key, algorithms=[algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            return http.HTTPException(status_code=401, detail="Invalid refresh token")
        user = get_user_by_id(db, user_id)
        if user is None:
            return http.HTTPException(status_code=404, detail="User not found")
        new_access_token = create_access_token(db,user_id, Secret_key, algorithm, expires_delta)
        return new_access_token
    except jwt.ExpiredSignatureError:
        return http.HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.JWTError:
        return http.HTTPException(status_code=401, detail="Invalid refresh token")