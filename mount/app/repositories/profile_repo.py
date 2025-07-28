from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Profile

from .base_repo import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
	def __init__(self, db: AsyncSession):
		super().__init__(db, Profile)
