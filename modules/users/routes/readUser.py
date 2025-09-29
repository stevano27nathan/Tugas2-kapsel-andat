# modules/users/routes/readUser.py
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional
from modules.users.schema.schemas import UserOut
from modules.users import models

router = APIRouter(prefix="/users", tags=["Users"])


def get_role(x_role: Optional[str] = Header(None)):
    if x_role is None:
        raise HTTPException(status_code=422, detail="X-role header required")
    if x_role not in ("admin", "staff"):
        raise HTTPException(status_code=403, detail="Invalid role")
    return x_role


def get_user_id(x_user_id: Optional[str] = Header(None)):
    # For endpoints that need to know the caller's id (staff), header can be required by caller
    return x_user_id


@router.get("/", response_model=list[UserOut])
def read_all_users(role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can read all users")
    return models.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, role: str = Depends(get_role), x_user_id: Optional[str] = Depends(get_user_id)):
    user = models.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # If caller is staff, allow only if requesting own resource
    if role == "staff":
        if not x_user_id:
            raise HTTPException(status_code=422, detail="X-user-id header required for staff")
        if x_user_id != user_id:
            raise HTTPException(status_code=403, detail="Staff can only read own data")
    return user
