from pydantic import BaseModel
from typing import Optional
from .roles import RoleResponse
from .profiles import ProfileResponse
from app.enums.roles import RoleEnum


class UserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: RoleEnum


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        form_attribute = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    role: Optional[RoleResponse] = None
    profile: Optional[ProfileResponse] = None

    class Config:
        form_attribute = True 


class UserWithRoleId(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    role_id: int

    class Config:
        form_attribute = True 


class LoginRequest(BaseModel):
    identifier: str 
    password: str 



