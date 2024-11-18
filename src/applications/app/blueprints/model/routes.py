from flask import Blueprint, jsonify, render_template, session, request, current_app
import logging 
import os

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
            logging.info('-----------------Upload file post--------------------------')
            if 'file' not in request.files:
                logging.warning('Aucun fichier trouvé dans la requête.')
                return jsonify({'error': 'Aucun fichier trouvé !'}), 400

            file = request.files['file']
            logging.info(file)

            if file.filename == '':
                logging.warning('Nom de fichier vide.')
                return jsonify({'error': 'Nom de fichier vide !'}), 400

            if not allowed_file(file.filename):
                logging.warning(f"Type de fichier non autorisé : {file.filename}")
                return jsonify({'error': 'Type de fichier non autorisé !'}), 400

            try:
                # Enregistrer le fichier dans le dossier spécifié
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                
                logging.info(file_path)
                logging.info(f"Fichier téléversé avec succès : {file.filename}")

                return jsonify({
                    'message': 'Fichier téléversé avec succès !',
                    'filename': file.filename
                }), 200

            except Exception as e:
                    logging.error(f"Erreur lors du téléversement du fichier : {e}")
                    return jsonify({'error': 'Une erreur est survenue lors du téléversement.'}), 500

            #return "post" 
        # get
        return render_template('model/upload.html')
    return "Pas connecté."