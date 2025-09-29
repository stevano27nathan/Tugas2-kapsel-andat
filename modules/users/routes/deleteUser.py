# modules/users/routes/deleteUser.py
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional
from modules.users import models

router = APIRouter(prefix="/users", tags=["Users"])


def get_role(x_role: Optional[str] = Header(None)):
    if x_role is None:
        raise HTTPException(status_code=422, detail="X-role header required")
    if x_role not in ("admin", "staff"):
        raise HTTPException(status_code=403, detail="Invalid role")
    return x_role


@router.delete("/{user_id}")
def delete_user(user_id: str, role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")
    ok = models.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted"}
