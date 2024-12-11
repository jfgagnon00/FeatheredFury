from io import BytesIO
import logging

from pathlib import Path
import ffury
from ffury.configs import DEFAULT_CONFIG_FILE, load_config
from ffury.transforms.spectrogram import spectrogram_from_audio
from ffury.transforms.waveform import waveform_apply_config

# import ffury
# from ffury.configs import (
#     DatasetType,
#     DEFAULT_CONFIG_FILE,
#     load_config
# )
#from ffury.dataset import IndexedDataset



from flask import Flask, current_app, request, jsonify
import os
import base64

import librosa
import matplotlib
matplotlib.use('Agg')  # Ou 'Qt5Agg' ou 'WebAgg'
from matplotlib import pyplot as plt
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = ".\\uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ApiController:
    def __init__(self):
        # self.upload_folder = './uploads'
        # if not os.path.exists(self.upload_folder):
        #     os.makedirs(self.upload_folder)
        # # Configurer le logging
        # logging.basicConfig(level=logging.DEBUG)
        pass
 
    @staticmethod    
    def index():
        return {
            "message": "Hello World!",
            "status": "API is running",
            "version": "1.0.0"
        }

    def waveform(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']

        # Logs détaillés pour analyse
        current_app.logger.info(f"*******************-----------------******************")
        current_app.logger.info(f"Nom brut du fichier reçu : {file.filename}")
        current_app.logger.info(f"Type de contenu : {file.content_type}")
        current_app.logger.info(f"Taille du fichier : {file.stream.tell()}")
        current_app.logger.info(f"*******************-----------------******************")
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:



            # creation config - on sait que DEFAULT_CONFIG_FILE est dans le repertoire parent
            config = Path(ffury.__file__).parents[2].joinpath(DEFAULT_CONFIG_FILE) 
            config = load_config(config)

            current_app.logger.info(f"***************config @@@@@@@@@@@@@@@@ : {config}")
            #utiliser JF function
            audio =  waveform_apply_config(file, config.preprocess.clip_sampling_rate_hz, config.preprocess) 
            #convertir en base64
            # shape du spectrogram est (n_mels, n_frames)
            # n_frames represente le temps
    
            S_db =  spectrogram_from_audio(audio, config.preprocess.clip_sampling_rate_hz, config.preprocess)
            #convertir en base64

            
            response_data = {"image_waveform": audio, 'image_spectogramme':S_db}
 
            return jsonify(response_data)



            # Sécuriser le nom du fichier
            #original_filename = secure_filename(file.filename) # Sauvegarder le fichier
            save_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(save_path)

            current_app.logger.info(f"******************* Fichier sauvegardé sous : {save_path}")

            # Générer l'image du waveform en base64
            waveform_base64 = self._generate_waveform_base64(save_path)
            spectogramme_base64 = self._generate_spectogramme_base64(save_path)
            
            response_data = {"image_waveform": waveform_base64, 'image_spectogramme':spectogramme_base64}
 
            return jsonify(response_data)
            
    #todo rendre private (ou mettre dans un service)
    #todo utiliser la generation de specto fait JF
    def _generate_spectogramme_base64(self, file_path):
        try:
            # Charger le fichier audio
            y, sr = librosa.load(file_path, sr=None)

            # Calculer le spectrogramme
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
            S_dB = librosa.power_to_db(S, ref=np.max)

            # Créer l'image du spectrogramme 
            fig, ax = plt.subplots(figsize=(10, 4))
            img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000, cmap='viridis', ax=ax)
            ax.set_title('Spectrogramme Mel')
            fig.colorbar(img, ax=ax, format='%+2.0f dB')
            plt.tight_layout()

            # Sauvegarder l'image dans un buffer en mémoire
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close(fig)
 
            # Encoder en base64
            spectogramme_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close() 
            return spectogramme_base64

        except Exception as e:
            logging.error(f"Erreur lors de la génération du spectogramme: {str(e)}")
            raise
    
    def _generate_waveform_base64(self, file_path):
        try:
            # Charger le fichier audio
            y, sr = librosa.load(file_path, sr=None)

            # Créer la figure pour afficher le waveform
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(np.linspace(0, len(y) / sr, len(y)), y)
            ax.set_title('Waveform')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')

            # Sauvegarder dans un buffer mémoire
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close(fig)

            # Encoder en base64
            waveform_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            return waveform_base64

        except Exception as e:
            logging.error(f"Erreur lors de la génération du waveform: {str(e)}")
            raise