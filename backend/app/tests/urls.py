from argparse import Namespace

from app.core.settings import test_settings
from app.main import create_app


class ApiUrl(str):
    __slots__ = ("path",)

    def __init__(self, path):
        self.path: str = path

    def __call__(self, *args, **kwargs):
        return self.path.format(*args, **kwargs)

    def __str__(self):
        return self.path


app = create_app(test_settings)
urls = Namespace(**{getattr(rout, "name"): ApiUrl(getattr(rout, "path")) for rout in app.routes})
