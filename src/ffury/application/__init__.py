from flask import Flask
from pathlib import Path

from .blueprints.home.routes import home
from .blueprints.auth.routes import auth
from .blueprints.model.routes import model
# from app.blueprints.predict.routes import predict

from ..configs import ProjectConfig

def create_flask_app(project_config: ProjectConfig,
                     secret: str) -> Flask:
    upload = Path.joinpath(project_config.paths.BUILD_DIR, "upload")
    upload.mkdir(parents=True, exist_ok=True)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = secret
    app.config["UPLOAD_FOLDER"] = upload
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 Mo
    app.config["ALLOWED_EXTENSIONS"] = {"wav", "mp3", "ogg"}

    # Enregistrer les Blueprints
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(model, url_prefix="/model")
    # app.register_blueprint(predict, url_prefix="/predict")

    return app
