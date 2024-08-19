from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.services.connection import get_db
from .BaseRepo import BaseRepo
from app.models.todos import Todo

class TodoRepo(BaseRepo[Todo]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Todo)
