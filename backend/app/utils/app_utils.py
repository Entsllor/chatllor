from argparse import Namespace

from fastapi import FastAPI


class ApiUrl(str):
    __slots__ = ("path",)

    def __init__(self, path):
        self.path: str = path

    def __call__(self, *args, **kwargs):
        return self.path.format(*args, **kwargs)

    def __str__(self):
        return self.path


def get_app_urls(app: FastAPI):
    return Namespace(**{getattr(rout, "name"): ApiUrl(getattr(rout, "path")) for rout in app.routes})
