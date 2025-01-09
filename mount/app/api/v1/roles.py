from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.schemas.users import UserRequest, UserResponse
from app.usecases import users as users_usecases
from typing import Optional


router = APIRouter(prefix="/roles")


@router.get("/")
async def all_roles(
    db: AsyncSession = Depends(get_db)
):
    resp = await users_usecases.user_all(db=db)
    return {"data": resp}

