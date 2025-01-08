from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.schemas.users import UserRequest, UserResponse
from app.usecases import users as users_usecases

router = APIRouter(prefix="/users")


@router.get("/")
async def all_users():
    return {"msg": "all user test"}


@router.post("/", response_model=UserResponse)
async def signup(user_in: UserRequest, db: AsyncSession = Depends(get_db)):
    resp = await users_usecases.user_signup(user_in.model_dump(), db)
    return {"msg": resp}