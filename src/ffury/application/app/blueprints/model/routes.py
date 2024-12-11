import base64
import json
from flask import Blueprint, jsonify, render_template, session, request, current_app 
import logging   
import requests


model = Blueprint('model', __name__)#, template_folder='../templates/home')

# Configuration de la journalisation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Vérification des extensions de fichiers
def allowed_file(filename):
    logging.info('-------------------------------------------\n')
    logging.info(current_app)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@model.route('/uploadfile', methods=['GET', 'POST'])
def index():     
    user = session.get('user') 
    if  user :
        if request.method == 'POST': 
            if 'file' not in request.files:
                logging.warning('Aucun fichier trouvé dans la requête.')
                return jsonify({'error': 'Aucun fichier trouvé !'}), 400

            file = request.files['file']
            #logging.warning(f"----------------------------- debut :      fichier : {file.filename}")

            if file.filename == '':
                logging.warning('Nom de fichier vide.')
                return jsonify({'error': 'Nom de fichier vide !'}), 400

            if file:
                #headers = {'Content-Type': 'application/octet-stream'}   host="0.0.0.0"

                #todo Pour qu'une application dans un conteneur soit accessible depuis l'extérieur, elle doit écouter sur 0.0.0.0 et non 127.0.0.1
                #api : nom du conteneur
                # url_api='http://api:8080/api/waveform'
                url_api='http://127.0.0.1:8080/api/waveform'
                response = requests.post(url_api, files={'file': (file.filename, file.stream, file.content_type)})
                result = response.json()
                #logging.info(f"**************************** Fichier sauvegardé sous : {json.dumps(result, indent=4)}")
                images = {
                    'image_waveform' : result['image_waveform'], 
                    'image_spectogramme' : result['image_spectogramme'], 
                    #'file_audio' : file.filename # base64.b64encode(file.read()).decode('utf-8')
                }
                
                # Passer l'image base64 à la page HTML
                return render_template('model/waveformResponse.html', result=images)
                return render_template('waveform.html')
            # if not allowed_file(file.filename):
            #     logging.warning(f"Type de fichier non autorisé : {file.filename}")
            #     return jsonify({'error': 'Type de fichier non autorisé !'}), 400
        return render_template('model/upload.html')
    else :  
        return "Pas connecté."