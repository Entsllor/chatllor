from app.core.database import Base


class Model:
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)


class ModelInDB(Base, Model):
    __abstract__ = True

    def _get_primary_keys(self) -> dict:
        return {column.name: getattr(self, column.name, None)
                for column in self.__table__.primary_key.columns.values()}

    def __str__(self):
        pks = self._get_primary_keys()
        model_name = self.__class__.__name__
        properties_str = ", ".join(f'{key}={value}' for key, value in pks.items())
        return f'{model_name}({properties_str})'

    def __repr__(self):
        pks = self._get_primary_keys()
        properties = pks | {
            "_deleted": self._sa_instance_state.deleted,
            "_modified": self._sa_instance_state.modified,

        }
        model_name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        properties_str = ", ".join(f'{key}={value}' for key, value in properties.items())
        return f'{model_name}({properties_str})'
