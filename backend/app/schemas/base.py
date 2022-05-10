from pydantic import BaseModel

from app.utils.schemas import to_camel_with_lower_first_char


class BaseScheme(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel_with_lower_first_char
        allow_population_by_field_name = True
