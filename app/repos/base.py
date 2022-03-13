from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class ExpectedOneInstance(Exception):
    pass


class BaseAsyncDbRepo:
    def __init__(self, db: AsyncSession):
        self.db = db


class BaseAsyncCrudRepo(BaseAsyncDbRepo):
    model: Base

    async def get_many(self, _limit: int = None, _offset: int = None, **filter_by) -> list:
        result = await self.db.execute(select(self.model).filter_by(**filter_by).limit(_limit).offset(_offset))
        return result.scalars().all()

    async def get_one(self, raise_if_many: False, **filter_by) -> Base:
        limit = 2 if raise_if_many else 1
        instances = await self.get_many(_limit=limit, **filter_by)
        if raise_if_many and len(instances) > 2:
            raise ExpectedOneInstance
        if not instances:
            return None
        return instances[0]

    async def delete(self, **filter_by):
        await self.db.execute(delete(self.model).filter_by(**filter_by))

    async def update(self, new_values: dict, **filter_by):
        q = update(self.model).filter_by(filter_by)
        for key, value in new_values.items():
            q = q.values(key=value)
        q.execution_options(synchronize_session="fetch")
        await self.db.execute(q)

    async def create(self, **values):
        instance = self.model(**values)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance
