from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from app.core.database import Base
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound
from app.utils.options import GetManyOptions, GetOneOptions


async def get_many_by_query(db, q: Query, options: GetManyOptions | dict = None) -> list:
    if isinstance(options, dict):
        options = GetManyOptions(**options)
    elif options is None:
        options = GetManyOptions()
    if options.limit is not None:
        q = q.limit(options.limit)
    if options.offset is not None:
        q = q.offset(options.offset)
    result = await db.execute(q)
    return result.scalars().all()


async def get_one_by_query(db, q: Query, options: GetOneOptions | dict = None) -> Base:
    if isinstance(options, dict):
        options = GetOneOptions(**options)
    elif options is None:
        options = GetOneOptions()
    limit = 2 if options.raise_if_many else 1
    instances = await get_many_by_query(db, q=q, options=GetManyOptions(limit=limit))
    if options.raise_if_many and len(instances) > 2:
        raise ExpectedOneInstance
    if not instances:
        if options.raise_if_none:
            raise InstanceNotFound
        return None
    return instances[0]


async def delete_by_query(db: AsyncSession, q: Query):
    return await db.execute(q)


async def update_by_query(db: AsyncSession, q: Query):
    q.execution_options(synchronize_session="fetch")
    await db.execute(q)


async def create_instance(db: AsyncSession, instance):
    db.add(instance)
    await db.flush()
    await db.refresh(instance)
    return instance
