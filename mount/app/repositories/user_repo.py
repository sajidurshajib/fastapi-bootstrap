from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import User, Role
from .base_repo import BaseRepository
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)


    async def get_by_userneme_or_email(self, identifier:str):
        try:
            query = select(User).filter(or_(User.username == identifier, User.email == identifier))
            result = await self.db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise e


    async def get_with_role(self, user_id: int):
        try:
            query = select(User).options(joinedload(User.role)).filter(User.id == user_id)
            result = await self.db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise e
    

    async def search(self, key:str, role:str, is_active:bool, offset: int = None, limit: int = None):
        try:
            query = select(User).options(joinedload(User.role))
            query = query.filter(User.is_active == is_active)
            if role:
                query = query.filter(User.role.has(Role.role == role))
            if key:
                query = query.filter(
                                    or_(
                                        User.full_name.ilike(f"%{key}%"),
                                        User.username.ilike(f"%{key}%"),
                                        User.email.ilike(f"%{key}%")
                                    )
                                )
            query = query.limit(limit).offset(offset)

            result = await self.db.execute(query)
            
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def create(self, data: dict, commit: bool = True):
        try:
            item = self.model(**data)
            self.db.add(item)
            if commit:
                await self.db.commit()
                await self.db.refresh(item)
            res = await self.get_with_role(user_id=item.id)
            return res
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e