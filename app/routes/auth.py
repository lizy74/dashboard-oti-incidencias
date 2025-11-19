from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario
from app.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username, activo=True).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        password_actual = request.form.get('password_actual')
        password_nuevo = request.form.get('password_nuevo')
        password_confirmar = request.form.get('password_confirmar')
        
        if not current_user.check_password(password_actual):
            flash('Contraseña actual incorrecta', 'error')
        elif password_nuevo != password_confirmar:
            flash('Las contraseñas nuevas no coinciden', 'error')
        elif len(password_nuevo) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
        else:
            current_user.set_password(password_nuevo)
            db.session.commit()
            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('dashboard.index'))
    
    return render_template('cambiar_password.html')

@bp.route('/perfil')
@login_required
def perfil():
    """Ver perfil del usuario actual"""
    return render_template('auth/perfil.html')

@bp.route('/perfil/editar', methods=['POST'])
@login_required
def editar_perfil():
    """Editar información del perfil"""
    try:
        nombre_completo = request.form.get('nombre_completo')
        email = request.form.get('email')
        
        # Verificar que el email no esté usado por otro usuario
        if email != current_user.email:
            usuario_existente = Usuario.query.filter_by(email=email).first()
            if usuario_existente:
                flash('El email ya está en uso por otro usuario', 'error')
                return redirect(url_for('auth.perfil'))
        
        # Actualizar datos
        current_user.nombre_completo = nombre_completo
        current_user.email = email
        
        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar perfil: {str(e)}', 'error')
    
    return redirect(url_for('auth.perfil'))

