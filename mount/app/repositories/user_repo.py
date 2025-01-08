from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User  
from .base_repo import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)