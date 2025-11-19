from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.rol != 'superadmin':
            flash('No tienes permisos para acceder a esta sección', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.rol not in ['admin', 'superadmin']:
            flash('No tienes permisos para acceder a esta sección', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def practicante_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.rol != 'practicante':
            flash('No tienes permisos para acceder a esta sección', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function
