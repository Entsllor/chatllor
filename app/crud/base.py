import sqlalchemy

from app.core.database import Base
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound


async def get_many(model, db, _limit: int = None, _offset: int = None, filters: dict = None) -> list:
    filters = {} if filters is None else filters
    result = await db.execute(sqlalchemy.select(model).filter_by(**filters).limit(_limit).offset(_offset))
    return result.scalars().all()


async def get_one(model, db, raise_if_many=False, raise_if_none=False, filters: dict = None) -> Base:
    filters = {} if filters is None else filters
    limit = 2 if raise_if_many else 1
    instances = await get_many(model, db, _limit=limit, filters=filters)
    if raise_if_many and len(instances) > 2:
        raise ExpectedOneInstance
    if not instances:
        if raise_if_none:
            raise InstanceNotFound
        return None
    return instances[0]


async def delete(model, db, filters: dict):
    filters = {} if filters is None else filters
    await db.execute(sqlalchemy.delete(model).filter_by(**filters))


async def update(model, db, new_values: dict, filters):
    filters = {} if filters is None else filters
    q = sqlalchemy.update(model).filter_by(**filters)
    for key, value in new_values.items():
        q = q.values(key=value)
    q.execution_options(synchronize_session="fetch")
    await db.execute(q)


async def create(model, db, **values):
    instance = model(**values)
    db.add(instance)
    await db.flush()
    await db.refresh(instance)
    return instance
