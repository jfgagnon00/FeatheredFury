from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
import logging
 
# Configure the logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

auth = Blueprint('auth', __name__)#( ), template_folder='.../.../../templates/auth')

# Route pour la déconnexion
@auth.route('/logout')
def logout():
    logging.info(session) 
    session.clear()
    logging.info(" --------------------------------") 
    logging.info(session) 
    flash('Vous avez été déconnecté.')
    return redirect(url_for('home.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
  
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifier les informations d'identification
        user = get_user(username)
        logging.info(str(username) + " : " + password) 
        logging.info( user) 
        if user and check_password_hash(user['password'], password):          
            # Stocker l'utilisateur dans la session
            session['user'] = username
            flash('Connexion réussie !', 'success')
            return redirect(url_for('home.index'))  # Rediriger vers l'index
        else:
            # non authentifié
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
            #return redirect(url_for('home.index'))  # Rediriger vers l'index
  
    return render_template('auth/login.html')

## todo a deplacer peut etre
def get_user(username):
    """Récupère un utilisateur dans le fichier CSV."""
    if not os.path.exists(USERS_FILE):
        return None
    with open(USERS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return row
    return None

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Process registration
#         return redirect(url_for('auth.login'))
#     return render_template('register.html')
 
USERS_FILE = os.path.join(os.path.dirname(__file__), '../../db/users.csv')

@auth.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifier que le nom d'utilisateur n'existe pas déjà
        if user_exists(username):
            flash('Le nom d\'utilisateur existe déjà.', 'danger')
            return redirect(url_for('auth.register'))

        # Hacher le mot de passe
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Sauvegarder les informations dans le fichier CSV
        save_user(username, hashed_password)
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

def user_exists(username):
    """Vérifie si un utilisateur existe dans le fichier CSV."""
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return True
    return False

def save_user(username, password):
    """Sauvegarde un utilisateur dans le fichier CSV."""
    file_exists = os.path.exists(USERS_FILE)
    with open(USERS_FILE, 'a', newline='') as file:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})