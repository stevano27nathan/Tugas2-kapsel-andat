# modules/users/routes/updateUser.py
from fastapi import APIRouter, Depends, Header, HTTPException
from modules.users.schema.schemas import UserUpdate, UserOut
from typing import Optional
from modules.users import models

router = APIRouter(prefix="/users", tags=["Users"])


def get_role(x_role: Optional[str] = Header(None)):
    if x_role is None:
        raise HTTPException(status_code=422, detail="X-role header required")
    if x_role not in ("admin", "staff"):
        raise HTTPException(status_code=403, detail="Invalid role")
    return x_role


@router.patch("/{user_id}", response_model=UserOut)   # patch = partial update
def update_user(user_id: str, user: UserUpdate, role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update users")

    update_data = user.model_dump(exclude_unset=True)
    updated = models.update_user(user_id, update_data)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
