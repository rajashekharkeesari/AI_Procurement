import http
from Backend.models.Users import Users

'''
this module about users, it provides functions to manage users in the database. It includes functionality to retrieve, create, update, and delete users.
'''


def create_user(db, user):
    if isinstance(user, dict):
        user_obj = Users(
            username=user.get("username"),
            password=user.get("password"),
            role=user.get("role", "user"),
            employee_id=user.get("employee_id"),
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Compatibility alias used by the authentication service
create_user_fn = create_user

def get_user_by_id(db, user_id):
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_username(db, username):
    return db.query(Users).filter(Users.username == username).first()

def update_user(db, user_id, updated_user):
    user = get_user_by_id(db, user_id)
    try:
        if user:
            user.username = updated_user.username
            user.email = updated_user.email
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="User not found")
    
def delete_user(db, user_id):
    user = get_user_by_id(db, user_id)
    try:
        if user:
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        else:
            return http.HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        db.rollback()
        raise e
        return http.HTTPException(status_code=404, detail="User not found")

