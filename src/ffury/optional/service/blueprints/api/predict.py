from flask import (
    current_app,
    jsonify,
    request,
)
from pathlib import Path
from werkzeug.utils import secure_filename

from . import api

def log_error(message: str):
    current_app.config["LOGGER"].error(message)
    return jsonify(dict(error=message)), 400

@api.route("/predict", methods=["POST"]) 
def predict():
    """
    Classification espece oiseau a partir d'un fichier
    ---
    parameters:
        - file: fichier
          in: path
          type: file
          required: true
          description: Fichier pour faire la prediction

    responses:
        200:
            description: Détail du projet

        400:
            description: Erreur
    """
    if "file" not in request.files:
        return log_error("No file part")
    
    file = request.files["file"]
    if file.filename == "":
        return log_error("No selected file")
    
    logger = current_app.config["LOGGER"]
    logger.info(f"Fichier recu: {file.filename}, taille: {request.content_length}")

    filename = secure_filename(file.filename)
    filename = Path.joinpath( current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filename)

    waveform_b64, spectrogram_b64 = current_app.config["API_CONTROLLER"].predict(filename)

    response_data = dict(
        waveform_b64=waveform_b64,
        spectrogram_b64=spectrogram_b64
    )

    # effacer le fichier pour le momement
    filename.unlink()

    return jsonify(response_data)
