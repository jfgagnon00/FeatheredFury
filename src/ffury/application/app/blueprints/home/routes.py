from flask import Blueprint, render_template, session
import logging

home = Blueprint('home', __name__)#, template_folder='../templates/home')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@home.route('/', methods=['GET'])
def index(): 
    logging.info(session.get('user'))
    return render_template('home/index.html')
 