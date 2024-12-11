from functools import wraps
from flask import redirect, url_for, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Accès non autorisé. Vous avez été redirigé vers l\'accueil.', 'warning')
            return redirect(url_for('main.index'))  # Rediriger vers l'index
        return f(*args, **kwargs)
    return decorated_function

