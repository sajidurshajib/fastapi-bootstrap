from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/")
async def all_users():
    return {"msg": "all user test"}