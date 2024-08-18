from fastapi import APIRouter


router = APIRouter()

@router.get('/')
async def read_todo():
    return {'msg':'All todos'}