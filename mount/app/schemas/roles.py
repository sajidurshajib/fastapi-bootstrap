from pydantic import BaseModel
from typing import List

class RoleResponse(BaseModel):
    role: str
    permissions: List[str]

    class Config:
        form_attribute = True 