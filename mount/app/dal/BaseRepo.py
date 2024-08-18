from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepo(Generic[T]):
    def __init__(self, db: AsyncSession, model: T):
        self.db = db
        self.model = model

    async def get(self, id: int) -> Optional[T]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        query = select(self.model)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: T) -> T:
        obj = self.model(**obj_in.model_dump())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: int, obj_in: T) -> Optional[T]:
        obj = await self.get(id)
        if not obj:
            return None
        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, id: int) -> Optional[T]:
        obj = await self.get(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
