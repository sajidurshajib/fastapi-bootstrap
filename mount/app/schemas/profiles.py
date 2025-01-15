from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProfileBase(BaseModel):
    address: Optional[str] = None
    secondary_address: Optional[str] = None
    phone: Optional[str] = None
    secondary_phone: Optional[str] = None
    dob: Optional[date] = None 
    sex: Optional[str] = None


class ProfileResponse(ProfileBase):

    class Config:
        form_attribute = True 

class ProfileUpdate(ProfileBase):

    class Config:
        form_attribute = True 
