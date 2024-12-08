from flask import Flask
import os
from app.blueprints.home.routes import home
from app.blueprints.auth.routes import auth
from app.blueprints.model.routes import model
# from app.blueprints.predict.routes import predict

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'votre_cle_secrete'
    app.config['UPLOAD_FOLDER'] = 'uploads'

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Taille maximale autorisée pour les fichiers (en octets)
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4 Mo

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # Extensions autorisées
    app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'ogg'}



    # Enregistrer les Blueprints
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(model, url_prefix='/model')
    # app.register_blueprint(predict, url_prefix='/predict')

    return app
