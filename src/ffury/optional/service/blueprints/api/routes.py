from flask import Flask

from . import api
from .index import index
from .predict import predict
from .validation import validation


def register_blueprint(app: Flask,
                       url_prefix: str) -> None:
    app.register_blueprint(api, url_prefix=url_prefix)
