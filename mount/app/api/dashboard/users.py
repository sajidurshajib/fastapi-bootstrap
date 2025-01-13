from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.schemas import StandardResponse
from app.schemas.users import UserRequest, LoginRequest
from app.utils.responses import standard_response
from app.usecases import users as users_usecases
from app.services.auth_dependency import logged_in, has_permission



router = APIRouter(prefix="/users")


@router.get("/search")
async def search_users(
    user: StandardResponse = Depends(has_permission("dashboard:users:search")),
    db: AsyncSession = Depends(get_db)
    ):
    status_code, success, message,  user_data = user
    return standard_response(status_code, success, message, user_data)

