from pydantic import BaseModel
from typing import Optional


class UserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: str



class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    role: Optional[str] = None 

    class Config:
        form_attribute = True 


class UserWithRoleId(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role_id: int


