from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dal.TodoRepo import TodoRepo  
from app.dto.TodoDTO import TodoResponse, TodoRequest

async def get_todos(db: AsyncSession) -> TodoResponse:
    todo_repo = TodoRepo(db=db)
    todos = await todo_repo.get_all()
    if not todos:
        raise HTTPException(status_code=404, detail="Todos not found")
    return todos


async def create_todo(todo_in: TodoRequest, db: AsyncSession) -> TodoResponse:
    todo_repo = TodoRepo(db=db)
    return await todo_repo.create(todo_in)