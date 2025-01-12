from base64 import b64encode
from ffury.optional.application.misc.errors import log_error
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

        # necesaire pour obtenir le contenu audio
        file.seek(0)
        result = response.json()

        # formater nombres pour simplifier affichage
        for p in result["predictions"]:
            p["time"] = round(p["time"] / 1000, 1)
            p["probabilities"] = [round(p, 4) for p in p["probabilities"]]

        print( "Num predictions", len(result["predictions"]) )

        # Passer l'image base64 à la page HTML
        return render_template("service/waveformResponse.html",
                               filename=file.filename,
                               waveform_b64=result["waveform_b64"],
                               spectrogram_b64=result["spectrogram_b64"],
                               predictions=result["predictions"],
                               audio_content_b64=b64encode(file.read()).decode("utf-8"),
                               audio_content_type=file.content_type)
    
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
    return render_template("/")
