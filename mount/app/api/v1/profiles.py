from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.services.auth_dependency import logged_in
from app.schemas import StandardResponse    
from app.schemas.profiles import ProfileUpdate
from app.utils.responses import standard_response
from app.usecases import profiles as profiles_usecases
import json

router = APIRouter(prefix="/profiles")


@router.get("/")
async def get_profile(user: StandardResponse = Depends(logged_in), db:AsyncSession = Depends(get_db)):
    user_status_code, user_success, user_message, user_data = user
    if not user_success:
        return standard_response(user_status_code, user_success, user_message, user_data)
    user_id = json.loads(user_data)["id"]
    status_code, success, message, data = await profiles_usecases.get_profile(user_id, db)
    return standard_response(status_code, success, message, data)


@router.patch("/update")
async def update(profile_in: ProfileUpdate, user: StandardResponse = Depends(logged_in), db:AsyncSession = Depends(get_db)):
    user_status_code, user_success, user_message, user_data = user
    if not user_success:
        return standard_response(user_status_code, user_success, user_message, user_data)
    user_id = json.loads(user_data)["id"]
    status_code, success, message, data = await profiles_usecases.update(user_id, profile_in, db)
    return standard_response(status_code, success, message, data)