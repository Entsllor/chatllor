from sqlalchemy import select, delete, update

from app.core.database import Base
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound


class BaseAsyncDbRepo:
    pass


class BaseAsyncCrudRepo(BaseAsyncDbRepo):
    model: Base

    async def get_many(self, db, _limit: int = None, _offset: int = None, **filter_by) -> list:
        result = await db.execute(select(self.model).filter_by(**filter_by).limit(_limit).offset(_offset))
        return result.scalars().all()

    async def get_one(self, db, raise_if_many=False, raise_if_none=False, **filter_by) -> Base:
        limit = 2 if raise_if_many else 1
        instances = await self.get_many(db, _limit=limit, **filter_by)
        if raise_if_many and len(instances) > 2:
            raise ExpectedOneInstance
        if not instances:
            if raise_if_none:
                raise InstanceNotFound
            return None
        return instances[0]

    async def delete(self, db, **filter_by):
        await db.execute(delete(self.model).filter_by(**filter_by))

    async def update(self, db, new_values: dict, **filter_by):
        q = update(self.model).filter_by(**filter_by)
        for key, value in new_values.items():
            q = q.values(key=value)
        q.execution_options(synchronize_session="fetch")
        await db.execute(q)

    async def create(self, db, **values):
        instance = self.model(**values)
        db.add(instance)
        await db.flush()
        await db.refresh(instance)
        return instance
