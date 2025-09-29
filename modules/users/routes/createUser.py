# modules/users/routes/createUser.py
from fastapi import APIRouter, status, HTTPException
from modules.users.schema.schemas import UserCreate, UserOut
from modules.users import models
import uuid

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    if models.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # generate unique id di route
    user_id = str(uuid.uuid4())

    # create user pakai user_id
    new_user = models.create_user(user, user_id=user_id)

    # hide password di response
    return {k: v for k, v in new_user.items() if k != "password"}

