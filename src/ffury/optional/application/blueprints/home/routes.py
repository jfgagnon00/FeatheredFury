from flask import Flask

from . import home
from .index import index
from .politic import politic
from .upload import upload


def register_blueprint(app: Flask,
                       url_prefix: str) -> None:
    app.register_blueprint(home, url_prefix=url_prefix)
