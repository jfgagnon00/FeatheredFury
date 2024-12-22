from flask import (
    current_app,
    render_template,
    request,
)
from pathlib import Path
from requests import post
from werkzeug.exceptions import RequestEntityTooLarge

from . import home


def allowed_file(filename: str) -> bool :
    return Path(filename).suffix.lower() in current_app.config["ALLOWED_EXTENSIONS"]

def log_error(message: str):
    current_app.config["LOGGER"].error(message)
    return render_template("errors/oups.html",
                           error_message=message)

def upload_file(file):
    if file.filename == "":
        return log_error("Nom de fichier vide."), 400

    if not allowed_file(file.filename):
        return log_error(f"Type de fichier non autorisé : {file.filename}"), 400

    try:
        response = post(current_app.config["SERVICE_CONFIG"].predict_url,
                        files={"file": (file.filename, file.stream, file.content_type)})

        if response.status_code != 200:
            return log_error(response.text), 400

        result = response.json()
        images = {
            "image_waveform" : result["image_waveform"],
            "image_spectogramme" : result["image_spectogramme"],
            #"file_audio" : file.filename # base64.b64encode(file.read()).decode("utf-8")
        }

        # Passer l'image base64 à la page HTML
        return render_template("service/waveformResponse.html",
                                result=images)
    except Exception as e:
        return log_error(repr(e)), 400

@home.route("/upload", methods=["GET", "POST"])
def upload():
    try:
        if request.method == "POST":
            if "file" not in request.files:
                return log_error("Aucun fichier trouvé dans la requête."), 400
            return upload_file(request.files["file"])
    except RequestEntityTooLarge:
        return log_error("Taille maximale depasse"), 400

    # method GET
    return render_template("home/index.html",
                           allowed_extensions=", ".join(current_app.config["ALLOWED_EXTENSIONS"]),
                           max_centent_length=current_app.config["MAX_CONTENT_LENGTH"] // 1024 // 1024)
