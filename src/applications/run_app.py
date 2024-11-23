# # from flask import Flask
# # from app.config.config import get_config_by_name
# # from app.initialize_functions import initialize_route, initialize_db, initialize_swagger

# # def create_app(config=None) -> Flask:
# #     """
# #     Create a Flask application.

# #     Args:
# #         config: The configuration object to use.

# #     Returns:
# #         A Flask application instance.
# #     """
# #     app = Flask(__name__)
# #     if config:
# #         app.config.from_object(get_config_by_name(config))

# #     # Initialize extensions
# #     initialize_db(app)

# #     # Register blueprints
# #     initialize_route(app)

# #     # Initialize Swagger
# #     initialize_swagger(app)

# #     return app


# # from flask import Flask
# # app = Flask(__name__)


# # @app.route("/")
# # def hello():
# # 	fic = open("modele.txt")
# # 	lignes = fic.readlines()
# # 	chaine = ""
# # 	for ligne in lignes:
# # 		chaine += ligne
# # 		return "Bienvenue monde!:"+chaine


# # if __name__ == "__main__":
# # 	app.run(host='0.0.0.0')



# from os import environ



# import os
# from flask import Flask, request, render_template, send_from_directory, redirect, url_for
# from werkzeug.utils import secure_filename
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# from datetime import datetime

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static'
# app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # Limite de 4 Mo pour les fichiers

# ALLOWED_EXTENSIONS = {'wav', 'mp3'}



# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/home')
# def home():
#     """Renders the home page."""
#     return render_template(
#         'index.html',
#         title='Home Page',
#         year=datetime.now().year,
#     )

# @app.route('/')
# def index():
#     """Renders the home page."""
#     return render_template(
#         'index.html',
#         title='Home Page',
#         year=datetime.now().year,
#     )

# @app.route('/contact')
# def contact():
#     """Renders the contact page."""
#     return render_template(
#         'contact.html',
#         title='Contact',
#         year=datetime.now().year,
#         message='Your contact page.'
#     )

# @app.route('/about')
# def about():
#     """Renders the about page."""
#     return render_template(
#         'about.html',
#         title='About',
#         year=datetime.now().year,
#         message='Your application description page.'
#     )

# @app.route('/upload_file', methods=['GET'])#, 'POST'
# def upload_file():
#     # if request.method == 'POST':
#     #     # Vérifie si un fichier a été uploadé
#     #     if 'file' not in request.files:
#     #         return "No file part", 400
#     #     file = request.files['file']

#     #     # Vérifie si le fichier est valide
#     #     if file.filename == '':
#     #         return "No selected file", 400
#     #     if file and allowed_file(file.filename):
#     #         filename = secure_filename(file.filename)
#     #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     #         file.save(filepath)

#     #         # Génération du spectrogramme
#     #         y, sr = librosa.load(filepath)
#     #         plt.figure(figsize=(10, 4))
#     #         S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
#     #         librosa.display.specshow(librosa.power_to_db(S, ref=np.max), sr=sr, x_axis='time', y_axis='mel')
#     #         plt.colorbar(format='%+2.0f dB')
#     #         spectrogram_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_spectrogram.png")
#     #         plt.savefig(spectrogram_path)
#     #         plt.close()

#     #         return redirect(url_for('display_image', filename=f"{filename}_spectrogram.png"))

#     return render_template('upload.html')

# @app.route('/static/<filename>')
# def display_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # if __name__ == "__main__":
# #     app.run(debug=True)

#from flask import render_template
from app import create_app

# Créer l'application Flask
app = create_app()


if __name__ == "__main__":
    # Lancer le serveur
    app.run(debug=True)

# if __name__ == '__main__':
#     HOST = environ.get('SERVER_HOST', 'localhost')
#     try:
#         PORT = int(environ.get('SERVER_PORT', '5555'))
#     except ValueError:
#         PORT = 5555
#     app.run(HOST, PORT, debug=True)
 
