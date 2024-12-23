from flask import Flask
from flasgger import Swagger
from ffury.configs import ProjectConfig
from ffury.misc.logging import (
    pretty_format,
    create_logger
)
from pathlib import Path

from .ServiceController import ServiceController
from .blueprints.api.routes import register_blueprint


def create_flask_app(project_config: ProjectConfig) -> Flask:
    upload = Path.joinpath(project_config.paths.BUILD_DIR, "upload")
    upload.mkdir(parents=True, exist_ok=True)

    app = Flask(__name__)
    app.config["PROJECT_CONFIG"] = project_config
    app.config["UPLOAD_FOLDER"] = upload
    app.config["CONTROLLER"] = ServiceController(project_config)
    app.config["LOGGER"] = create_logger(name=__name__)
    app.config["SWAGGER"] = dict(title=project_config.paths.PROJECT_NAME,
                                 version="0.0.1")

    register_blueprint(app, url_prefix="/api")

    message = pretty_format(app.config["CONTROLLER"].status)
    app.config["LOGGER"].info(message)

    return app, Swagger(app)
