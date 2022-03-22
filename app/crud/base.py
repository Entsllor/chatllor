from typing import Iterable

from sqlalchemy import select, update, insert, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from app.core.database import Base
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound
from app.utils.options import GetManyOptions, GetOneOptions


class BaseCrudDB:
    model: Base

    @property
    def _select(self) -> Query:
        return select(self.model)

    @property
    def _update(self) -> Query:
        return update(self.model)

    @property
    def _insert(self) -> Query:
        return insert(self.model)

    @property
    def _delete(self) -> Query:
        return delete(self.model)

    async def get_one(self, db: AsyncSession, _options: GetOneOptions = None, **filters):
        query = self._select.filter_by(**filters)
        return await get_one_by_query(db, query, options=_options)

    async def get_many(self, db: AsyncSession, _options: GetManyOptions = None, **filters):
        query = self._select.filter_by(**filters)
        return await get_many_by_query(db, query, options=_options)


def order_by_fields(query: Query, ordering_fields: Iterable[str]) -> Query:
    for ordering_field in ordering_fields:
        if ordering_field.startswith("-"):
            query = query.order_by(text(f'{ordering_field[1:]} desc'))
        else:
            query = query.order_by(text(f"{ordering_field} asc"))
    return query


async def get_many_by_query(db, q: Query, options: GetManyOptions | dict = None) -> list:
    if isinstance(options, dict):
        options = GetManyOptions(**options)
    elif options is None:
        options = GetManyOptions()
    if options.limit is not None:
        q = q.limit(options.limit)
    if options.offset is not None:
        q = q.offset(options.offset)
    if options.ordering_fields:
        q = order_by_fields(q, options.ordering_fields)
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


async def update_instance(db: AsyncSession, instance, **values):
    for key, value in values.items():
        setattr(instance, key, value)
    await db.flush(objects=[instance])
    await db.refresh(instance)
    return instance


async def create_instance(db: AsyncSession, instance):
    db.add(instance)
    await db.flush()
    await db.refresh(instance)
    return instance
