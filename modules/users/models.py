# modules/users/models.py
from datetime import datetime, timezone
import uuid
import bcrypt
from typing import Optional

# simple in-memory DB (list of dicts)
users_db: list[dict] = []


def _now():
    return datetime.now(timezone.utc)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_user(user_obj, user_id: str) -> dict:
    # Validasi role
    allowed_roles = {"staff", "admin"}  # Sesuaikan dengan roles yang diizinkan
    if user_obj.role not in allowed_roles:
        raise ValueError(f"Role '{user_obj.role}' tidak diizinkan. Harus salah satu dari: {allowed_roles}")
    
    user = {
        "id": user_id,
        "username": user_obj.username,
        "email": user_obj.email,
        "password": hash_password(user_obj.password),
        "role": user_obj.role.value if hasattr(user_obj.role, "value") else user_obj.role,
        "created_at": _now(),
        "updated_at": _now(),
    }
    users_db.append(user)
    return user


def get_all_users() -> list[dict]:
    # return copies without password for safety
    return [{k: v for k, v in u.items() if k != "password"} for u in users_db]


def get_user_by_id(user_id: str, hide_password: bool = True) -> Optional[dict]:
    u = next((x for x in users_db if x["id"] == user_id), None)
    if not u:
        return None
    if hide_password:
        return {k: v for k, v in u.items() if k != "password"}
    return u


def get_user_by_username(username: str) -> Optional[dict]:
    return next((x for x in users_db if x["username"] == username), None)


def update_user(user_id, update_data):
    user = get_user_by_id(user_id, hide_password=False)  # Need actual user object
    if user:
        # Validasi jika mengupdate role
        if 'role' in update_data:
            allowed_roles = {"staff", "admin"}
            if update_data['role'] not in allowed_roles:
                raise ValueError(f"Role '{update_data['role']}' tidak diizinkan")
        
        for key, value in update_data.items():
            user[key] = value
        user["updated_at"] = _now()  # Update timestamp
        return user
    return None

def validate_user_role(user_id: str, expected_role: str) -> bool:
    """Validasi apakah user memiliki role yang diharapkan"""
    user = get_user_by_id(user_id)
    return user and user.get("role") == expected_role

def delete_user(user_id: str) -> bool:
    global users_db
    before = len(users_db)
    users_db = [u for u in users_db if u["id"] != user_id]
    return len(users_db) < before
