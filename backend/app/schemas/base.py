from pydantic import BaseModel
from pydantic.utils import to_camel


def to_camel_with_lower_first_char(string):
    if len(string) > 1:
        return string[:1] + to_camel(string)[1:]
    return string


class BaseScheme(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel_with_lower_first_char
        allow_population_by_field_name = True
