from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.schemas.users import UserRequest, UserResponse
from app.usecases import users as users_usecases
from typing import Optional


router = APIRouter(prefix="/users")


@router.get("/")
async def all_users(
    email: Optional[str] = Query(None),
    username: Optional[str] = Query(None),
    full_name: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    resp = await users_usecases.all(
        db=db, 
        limit=limit, 
        offset=offset, 
        email=email, 
        username=username, 
        full_name=full_name
        )
        
    return {"data": resp}


@router.post("/", response_model=UserResponse)
async def signup(
    user_in: UserRequest, 
    db: AsyncSession = Depends(get_db)
    ):
    resp = await users_usecases.user_signup(user_in.model_dump(), db)
    return {"msg": resp}