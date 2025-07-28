from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar('T')


class BaseRepository(Generic[T]):
	def __init__(self, db: AsyncSession, model: Type[T]):
		self.db = db
		self.model = model

	async def get_by_field(self, field_name: str, value: any) -> Optional[T]:
		try:
			query = select(self.model).filter(
				getattr(self.model, field_name) == value
			)
			result = await self.db.execute(query)
			return result.scalars().first()
		except SQLAlchemyError as e:
			raise e

	async def get_all_by_field(
		self,
		field_name: str,
		value: any,
		limit: Optional[int] = None,
		offset: Optional[int] = None,
	) -> List[T]:
		try:
			query = select(self.model).filter(
				getattr(self.model, field_name) == value
			)

			if limit is not None:
				query = query.limit(limit)
			if offset is not None:
				query = query.offset(offset)

			result = await self.db.execute(query)
			return result.scalars().all()

		except SQLAlchemyError as e:
			raise e

	async def get_all_by_multi_fields(
		self,
		limit: Optional[int] = None,
		offset: Optional[int] = None,
		**kwargs,
	) -> List[T]:
		try:
			# Pop limit and offset from kwargs if passed as part of **kwargs
			limit = kwargs.pop('limit', limit)
			offset = kwargs.pop('offset', offset)

			query = select(self.model)
			for field, value in kwargs.items():
				if value is not None:
					query = query.filter(getattr(self.model, field) == value)

			if limit is not None:
				query = query.limit(limit)
			if offset is not None:
				query = query.offset(offset)

			result = await self.db.execute(query)
			return result.scalars().all()

		except SQLAlchemyError as e:
			raise e

	async def get_all(
		self, skip: int = 0, limit: int = 100, all: bool = False
	) -> List[T]:
		try:
			if not all:
				result = await self.db.execute(
					select(self.model).offset(skip).limit(limit)
				)
			else:
				result = await self.db.execute(select(self.model))
			return result.scalars().all()
		except SQLAlchemyError as e:
			raise e

	async def create(self, data: dict, commit: bool = True) -> T:
		try:
			item = self.model(**data)
			self.db.add(item)
			if commit:
				await self.db.commit()
				await self.db.refresh(item)
			return item
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

	async def update(self, item_id: str, updated_data: dict) -> Optional[T]:
		try:
			result = await self.db.execute(
				select(self.model).filter(self.model.id == item_id)
			)
			item = result.scalars().first()
			if not item:
				return None

			for key, value in updated_data.items():
				setattr(item, key, value)

			await self.db.commit()
			await self.db.refresh(item)
			return item
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e

	async def delete(self, field_name: str, field_value: any) -> bool:
		try:
			field = getattr(self.model, field_name)
			result = await self.db.execute(
				select(self.model).filter(field == field_value)
			)
			item = result.scalars().first()
			if not item:
				return False

			await self.db.delete(item)
			await self.db.commit()
			return True
		except SQLAlchemyError as e:
			await self.db.rollback()
			raise e
