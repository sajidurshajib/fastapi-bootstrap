from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.connection import get_db
from app.usecases.todo import get_todos, create_todo
from typing import List
from app.dto.TodoDTO import TodoResponse

router = APIRouter()

@router.get('/', response_model=List[TodoResponse])
async def read_todos(db: AsyncSession = Depends(get_db)):
    return await get_todos(db)


@router.post('/', response_model=TodoResponse)
async def create(todo_in: TodoResponse, db: AsyncSession = Depends(get_db)):
    return await create_todo(todo_in, db)