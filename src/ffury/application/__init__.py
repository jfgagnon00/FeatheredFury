from flask import Flask
from pathlib import Path

from ..configs import ProjectConfig
from ..misc.logging import create_logger

from .blueprints.home.routes import register_blueprint


def create_flask_app(project_config: ProjectConfig,
                     secret: str) -> Flask:
    upload = Path.joinpath(project_config.paths.BUILD_DIR, "upload")
    upload.mkdir(parents=True, exist_ok=True)

    app = Flask(__name__)
    app.config["SERVICE_SECRET"] = secret
    app.config["SERVICE_CONFIG"] = project_config.service
    app.config["UPLOAD_FOLDER"] = upload
    app.config["MAX_CONTENT_LENGTH"] = project_config.service.max_content_size
    app.config["ALLOWED_EXTENSIONS"] = project_config.service.allowed_extensions
    app.config["LOGGER"] = create_logger(file=__file__)

    register_blueprint(app, url_prefix="/")

    @app.context_processor
    def inject_context():
        return dict(name=project_config.paths.PROJECT_NAME, 
                    year=2024)

    return app
