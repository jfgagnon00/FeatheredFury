from flask import (
    Blueprint, 
    current_app,
    jsonify, 
    render_template, 
    request, 
)
from pathlib import Path
from requests import post


model = Blueprint("model", __name__)


# Vérification des extensions de fichiers
def allowed_file(filename: str) -> bool :
    return Path(filename).suffix.lower() in current_app.config["ALLOWED_EXTENSIONS"]

def log_error(message: str):
    current_app.config["LOGGER"].error(message)
    return jsonify({"error": message})


@model.route("/upload", methods=["GET", "POST"])
def index():
    if request.method == "POST": 
        if "file" not in request.files:
            return log_error("Aucun fichier trouvé dans la requête."), 400

        file = request.files["file"]
        if file.filename == "":
            return log_error("Nom de fichier vide."), 400
        
        if not allowed_file(file.filename):
            return log_error(f"Type de fichier non autorisé : {file.filename}"), 400

        response = post(current_app.config["SERVER_CONFIG"].waveform_url, 
                        files={"file": (file.filename, file.stream, file.content_type)})
        result = response.json()

        #logging.info(f"**************************** Fichier sauvegardé sous : {json.dumps(result, indent=4)}")
        images = {
            "image_waveform" : result["image_waveform"], 
            "image_spectogramme" : result["image_spectogramme"], 
            #"file_audio" : file.filename # base64.b64encode(file.read()).decode("utf-8")
        }
        
        # Passer l'image base64 à la page HTML
        return render_template("model/waveformResponse.html", result=images)

    return render_template("model/upload.html", 
                           allowed_extensions=current_app.config["ALLOWED_EXTENSIONS"])
