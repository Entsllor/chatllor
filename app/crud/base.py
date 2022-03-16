import sqlalchemy

from app.core.database import Base
from app.utils.options import GetManyOptions, GetOneOptions
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound


async def get_many(model, db, filters: dict = None, options: GetManyOptions | dict = None) -> list:
    if isinstance(options, dict):
        options = GetManyOptions(**options)
    elif options is None:
        options = GetManyOptions()
    filters = {} if filters is None else filters
    result = await db.execute(sqlalchemy.select(model).filter_by(**filters).limit(options.limit).offset(options.offset))
    return result.scalars().all()


async def get_one(model, db, filters: dict = None, options: GetOneOptions | dict = None) -> Base:
    if isinstance(options, dict):
        options = GetOneOptions(**options)
    elif options is None:
        options = GetOneOptions()
    filters = {} if filters is None else filters
    limit = 2 if options.raise_if_many else 1
    instances = await get_many(model, db, options=GetManyOptions(limit=limit), filters=filters)
    if options.raise_if_many and len(instances) > 2:
        raise ExpectedOneInstance
    if not instances:
        if options.raise_if_none:
            raise InstanceNotFound
        return None
    return instances[0]


async def delete(model, db, filters: dict):
    filters = {} if filters is None else filters
    await db.execute(sqlalchemy.delete(model).filter_by(**filters))


async def update(model, db, new_values: dict, filters):
    filters = {} if filters is None else filters
    q = sqlalchemy.update(model).filter_by(**filters).values(**new_values)
    q.execution_options(synchronize_session="fetch")
    await db.execute(q)


async def create(model, db, **values):
    instance = model(**values)
    db.add(instance)
    await db.flush()
    await db.refresh(instance)
    return instance
