from flask import Flask

from ffury.configs import ProjectConfig
from ffury.misc.logging import create_logger

from .blueprints.home.routes import register_blueprint


def create_flask_app(project_config: ProjectConfig) -> Flask:
    app = Flask(__name__)
    app.config["SERVICE_CONFIG"] = project_config.service
    app.config["MAX_CONTENT_LENGTH"] = project_config.service.max_content_size
    app.config["ALLOWED_EXTENSIONS"] = project_config.service.allowed_extensions
    app.config["LOGGER"] = create_logger(name=__name__)

    register_blueprint(app, url_prefix="/")

    @app.context_processor
    def inject_context():
        return dict(name=project_config.paths.PROJECT_NAME, 
                    year=2024)

    return app
