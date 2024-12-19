from flask import Flask
from pathlib import Path

from .blueprints.home.routes import home
from .blueprints.model.routes import model
# from app.blueprints.predict.routes import predict

from ..configs import ProjectConfig
from ..misc.logging import create_logger

def create_flask_app(project_config: ProjectConfig,
                     secret: str) -> Flask:
    upload = Path.joinpath(project_config.paths.BUILD_DIR, "upload")
    upload.mkdir(parents=True, exist_ok=True)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = secret
    app.config["UPLOAD_FOLDER"] = upload
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 Mo
    app.config["ALLOWED_EXTENSIONS"] = {"wav", "mp3", "ogg"}
    app.config["LOGGER"] = create_logger(file=__file__)

    # Enregistrer les Blueprints
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(model, url_prefix="/model")
    # app.register_blueprint(predict, url_prefix="/predict")

    @app.context_processor
    def inject_context():
        return dict(name=project_config.paths.PROJECT_NAME, 
                    year=2024)

    return app
