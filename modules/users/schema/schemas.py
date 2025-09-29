# modules/users/schema/schemas.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
from datetime import datetime
import re
from typing import Optional

class RoleEnum(str, Enum):
    admin = "admin"
    staff = "staff"

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=15, pattern="^[a-z0-9]+$")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=20)
    role: Optional[RoleEnum] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=6, max_length=15, pattern=r"^[a-z0-9]+$")
    email: EmailStr
    role: RoleEnum


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator("password")
    def check_password(cls, v: str) -> str:
        # hanya huruf, angka, !, @
        if not re.match(r"^[A-Za-z0-9!@]+$", v):
            raise ValueError("Password hanya boleh berisi huruf, angka, !, dan @")
        # minimal satu uppercase
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password harus mengandung huruf kapital")
        # minimal satu lowercase
        if not re.search(r"[a-z]", v):
            raise ValueError("Password harus mengandung huruf kecil")
        # minimal satu digit
        if not re.search(r"[0-9]", v):
            raise ValueError("Password harus mengandung angka")
        # minimal satu special ! atau @
        if not re.search(r"[!@]", v):
            raise ValueError("Password harus mengandung karakter spesial (! atau @)")
        return v


class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
