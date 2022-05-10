from typing import Type, Optional

from pydantic import ValidationError, BaseModel
from pydantic.fields import ModelField
from pydantic.utils import to_camel


def is_valid_schema(schema: Type[BaseModel], data, many=None) -> bool:
    if many is None:
        data = [data] if not isinstance(data, list | tuple) else data
    try:
        all(map(schema.validate, data))
    except ValidationError:
        return False
    return True


def to_camel_with_lower_first_char(string: str):
    if len(string) > 1:
        return string[:1].lower() + to_camel(string)[1:]
    return string


def partial(schema: Type[BaseModel]) -> Type[BaseModel]:
    """All fields of base classes become optional
    Use this as a decorator or as a function

    @partial
    class UserUpdate(UserCreate):
        'all fields is optional.'
        optional_field: int # anyway is partial

    # Alias:
    UserUpdate = partial(UserCreate)

    class UserUpdateWithRequiredField(partial(UserCreate)):
        'override base class'
        required_field: int # is required
        optional_field: int | None # is optional
        'other fields are optional'
    """

    class PartialSchema(schema):
        pass

    optional_fields = schema.__fields__.copy()
    for name, field, in optional_fields.items():
        optional_fields[name] = ModelField(
            name=field.name,
            type_=Optional[field.type_],
            class_validators=field.class_validators,
            model_config=field.model_config,
            default=field.default,
            default_factory=field.default_factory,
            required=False,
            alias=field.alias,
            field_info=field.field_info
        )

    PartialSchema.__fields__ |= optional_fields
    PartialSchema.__name__ = "Partial" + schema.__name__

    return PartialSchema


def is_partial(schema: BaseModel | Type[BaseModel]) -> bool:
    base = schema.__class__ if isinstance(schema, BaseModel) else schema
    try:
        base()  # try to make instance without arguments
    except (ValidationError, TypeError):
        return False
    return True
