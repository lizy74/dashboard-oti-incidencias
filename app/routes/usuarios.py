from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Usuario, Practicante
from app.extensions import db
from functools import wraps

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol != 'admin':
            flash('No tienes permisos', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def lista():
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    return render_template('usuarios.html', usuarios=usuarios)

@bp.route('/resetear-password/<int:id>', methods=['POST'])
@login_required
@admin_required
def resetear_password(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        nueva_password = request.form.get('nueva_password', usuario.username)
        
        usuario.set_password(nueva_password)
        db.session.commit()
        
        flash(f'Contraseña reseteada a: {nueva_password}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('usuarios.lista'))
