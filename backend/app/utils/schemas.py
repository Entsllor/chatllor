from typing import Type

from pydantic import ValidationError

from app.schemas.base import BaseScheme


def is_valid_schema(schema: Type[BaseScheme], data, many=None) -> bool:
    if many is None:
        data = [data] if not isinstance(data, list | tuple) else data
    try:
        all(map(schema.validate, data))
    except ValidationError:
        return False
    return True
