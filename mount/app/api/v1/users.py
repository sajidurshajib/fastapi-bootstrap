from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.schemas import StandardResponse
from app.schemas.users import UserRequest, UserUpdate, LoginRequest, UpdatePassword
from app.utils.responses import standard_response
from app.usecases import users as users_usecases
from app.services.auth_dependency import logged_in
import json

router = APIRouter(prefix="/users")


@router.get("/auth")
async def auth(
    user: StandardResponse = Depends(logged_in)
    ):
    status, success, message, data = user
    return standard_response(status, success, message, data)


@router.post("/signup", response_model=StandardResponse)
async def signup(
    user_in: UserRequest, 
    db: AsyncSession = Depends(get_db)
    ):
    status, success, message, data = await users_usecases.signup(user_in, db)
    return standard_response(status, success, message, data)


@router.post("/login", description="identifier: username_or_email")
async def login(
    user_credentials: LoginRequest, 
    db: AsyncSession = Depends(get_db)
    ):
    status, success, message, data = await users_usecases.login(user_credentials, db)
    return standard_response(status, success, message, data)


@router.patch("/update", response_model=StandardResponse)
async def update(
    user_in: UserUpdate, 
    user: StandardResponse = Depends(logged_in),
    db: AsyncSession = Depends(get_db)
    ):
    user_status_code, user_success, user_message, user_data = user
    if not user_success:
        return standard_response(user_status_code, user_success, user_message, user_data)
    user_id = json.loads(user_data)["id"]
    status_code, success, message, data = await users_usecases.update(user_id, user_in, db)
    return standard_response(status_code, success, message, data)


@router.patch("/update-password", response_model=StandardResponse)
async def update_password(
    pass_in: UpdatePassword, 
    user: StandardResponse = Depends(logged_in),
    db: AsyncSession = Depends(get_db)
    ):
    user_status_code, user_success, user_message, user_data = user
    if not user_success:
        return standard_response(user_status_code, user_success, user_message, user_data)
    user_id = json.loads(user_data)["id"]
    status_code, success, message, data = await users_usecases.update_password(pass_in.new_password, user_id, db, True, pass_in.old_password)
    return standard_response(status_code, success, message, data)   