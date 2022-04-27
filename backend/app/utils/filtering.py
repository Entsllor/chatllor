from typing import Type, Any, NamedTuple, Iterable

from fastapi import Request
from pydantic import BaseModel
from pydantic.fields import ModelField
from sqlalchemy import Integer, orm


class Filter(NamedTuple):
    field_name: str
    operator: str
    value: Any


def handle_filter_param(field: ModelField, value_to_parse: str) -> tuple[str, Any]:
    if issubclass(int, field.type_):
        match value_to_parse.split(":"):
            case "eq" | "ne" | "gt" | "ge" | "lt" | "le" as operator, value:
                return operator, value
            case [value]:
                return "eq", value
    elif issubclass(str, field.type_):
        match value_to_parse.split(":"):
            case "eq" | "ne" | "gt" | "ge" | "lt" | "le" | "like" as operator, value:
                return operator, value
            case [value]:
                return "eq", value
    raise ValueError("Failed to parse the parameter")


def filter_by_model(model: Type[BaseModel]):
    fields = model.__fields__

    def inner(request: Request):
        filters = []
        for param, value in request.query_params.items():
            if param not in fields:
                continue
            try:
                operator, value = handle_filter_param(fields[param], value)
            except ValueError:
                continue
            filters.append(Filter(param, operator, value))
        return filters

    return inner


FILTER_OPERATORS = {
    "eq": "__eq__",  # ==
    "ne": "__ne__",  # !=
    "gt": "__gt__",  # <
    "ge": "__ge__",  # <=
    "lt": "__lt__",  # >
    "le": "__le__",  # >=
    "like": "like",  # Model.column.like as SQL like
}


def add_filter(query: orm.Query, filter_: Filter) -> orm.Query:
    available_fields = {
        field.key: field for field in
        [field for table in query.get_final_froms() for field in table.columns]
    }
    value = filter_.value
    try:
        field = available_fields[filter_.field_name]
        operation = FILTER_OPERATORS[filter_.operator]
        criterion = getattr(field, operation, None)
        if isinstance(field.type, Integer):
            value = int(value)
    except (ValueError, KeyError, AttributeError):
        return query
    return query.where(criterion(value))


def set_filters(query: orm.Query, filters: Iterable):
    for filter_ in filters:
        query = add_filter(query, filter_)
    return query
