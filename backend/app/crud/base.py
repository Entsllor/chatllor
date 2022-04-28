import itertools
from typing import Iterable, Mapping

from sqlalchemy import select, update, insert, delete, text
from sqlalchemy.orm import Query

from app.core.database import Base, get_session
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound
from app.utils.filtering import set_filters
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

    async def get_one(self, _options: GetOneOptions = None, **filters) -> Base:
        query = self._select.filter_by(**filters)
        return await get_one_by_query(query, options=_options)

    async def get_many(self, _options: GetManyOptions = None, **filters) -> list[Base]:
        query = self._select.filter_by(**filters)
        return await get_many_by_query(query, options=_options)

    async def delete(self, **filters) -> int:
        query = self._delete.filter_by(**filters)
        return await delete_by_query(query)


def order_by_fields(query: Query, ordering_fields: Iterable[str]) -> Query:
    available_field = list(itertools.chain(*[fields.columns.keys() for fields in query.froms]))
    for field_name in ordering_fields:
        order = 'asc'
        if field_name.startswith('-'):
            order = 'desc'
            field_name = field_name.removeprefix('-')
        if field_name in available_field:
            query = query.order_by(text(f"{field_name} {order}"))
    return query


async def get_many_by_query(q: Query, options: GetManyOptions | Mapping = None) -> list:
    if isinstance(options, Mapping):
        options = GetManyOptions(**options)
    options = options or GetManyOptions()
    if options.limit is not None:
        q = q.limit(options.limit)
    if options.offset is not None:
        q = q.offset(options.offset)
    if options.ordering_fields:
        q = order_by_fields(q, options.ordering_fields)
    q = set_filters(q, options.filters)
    result = await get_session().execute(q)
    return result.scalars().all()


async def get_one_by_query(q: Query, options: GetOneOptions | Mapping = None) -> Base:
    if isinstance(options, Mapping):
        options = GetOneOptions(**options)
    options = options or GetOneOptions()
    limit = 2 if options.raise_if_many else 1
    instances = await get_many_by_query(q=q, options=GetManyOptions(limit=limit))
    if options.raise_if_many and len(instances) > 2:
        raise ExpectedOneInstance
    if not instances:
        if options.raise_if_none:
            raise InstanceNotFound
        return None
    return instances[0]


async def delete_by_query(q: Query) -> int:
    return (await get_session().execute(q)).rowcount


async def update_by_query(q: Query) -> int:
    q.execution_options(synchronize_session="fetch")
    return (await get_session().execute(q)).rowcount


async def update_instance(instance: Base, **values) -> Base:
    for key, value in values.items():
        setattr(instance, key, value)
    await get_session().flush(objects=[instance])
    await get_session().refresh(instance)
    return instance


async def create_instance(instance: Base) -> Base:
    get_session().add(instance)
    await get_session().flush()
    await get_session().refresh(instance)
    return instance
