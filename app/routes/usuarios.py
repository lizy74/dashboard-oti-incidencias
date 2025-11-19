from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Usuario, Practicante
from app.extensions import db
from app.decorators import admin_required


bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@bp.route('/')
@login_required
@admin_required
def lista():
    # Filtrar usuarios según el rol del usuario actual
    if current_user.rol == 'superadmin':
        # Super admin ve admins y practicantes
        usuarios = Usuario.query.filter(
            Usuario.rol.in_(['admin', 'practicante'])
        ).order_by(Usuario.fecha_creacion.desc()).all()
    elif current_user.rol == 'admin':
        # Admin solo ve practicantes
        usuarios = Usuario.query.filter_by(
            rol='practicante'
        ).order_by(Usuario.fecha_creacion.desc()).all()
    else:
        usuarios = []
    
    return render_template('usuarios.html', usuarios=usuarios)


@bp.route('/crear', methods=['POST'])
@login_required
@admin_required
def crear():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        nombre_completo = request.form.get('nombre_completo')
        password = request.form.get('password')
        rol = request.form.get('rol')
        
        # VALIDACIÓN DE SEGURIDAD
        # Admin solo puede crear practicantes
        if current_user.rol == 'admin' and rol != 'practicante':
            flash('Solo puedes crear usuarios practicantes', 'error')
            return redirect(url_for('usuarios.lista'))
        
        # Superadmin puede crear admin y practicante (NO superadmin)
        if current_user.rol == 'superadmin' and rol not in ['admin', 'practicante']:
            flash('Tipo de usuario no válido', 'error')
            return redirect(url_for('usuarios.lista'))
        
        # Verificar que no exista el usuario
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('usuarios.lista'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('usuarios.lista'))
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            rol=rol,
            activo=True
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash(f'Usuario {username} creado exitosamente. Contraseña: {password}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'error')
    
    return redirect(url_for('usuarios.lista'))


@bp.route('/resetear-password/<int:id>', methods=['POST'])
@login_required
@admin_required
def resetear_password(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        
        # VALIDACIÓN DE SEGURIDAD
        if usuario.rol == 'superadmin':
            flash('No puedes modificar cuentas de Super Admin', 'error')
            return redirect(url_for('usuarios.lista'))
        
        if current_user.rol == 'admin' and usuario.rol != 'practicante':
            flash('No tienes permisos para modificar este usuario', 'error')
            return redirect(url_for('usuarios.lista'))
        
        nueva_password = request.form.get('nueva_password', usuario.username)
        
        usuario.set_password(nueva_password)
        db.session.commit()
        
        flash(f'Contraseña de {usuario.username} reseteada a: {nueva_password}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('usuarios.lista'))


@bp.route('/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_estado(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        
        # VALIDACIÓN DE SEGURIDAD
        if usuario.rol == 'superadmin':
            flash('No puedes modificar cuentas de Super Admin', 'error')
            return redirect(url_for('usuarios.lista'))
        
        if current_user.rol == 'admin' and usuario.rol != 'practicante':
            flash('No tienes permisos para modificar este usuario', 'error')
            return redirect(url_for('usuarios.lista'))
        
        usuario.activo = not usuario.activo
        db.session.commit()
        
        estado = 'activado' if usuario.activo else 'desactivado'
        flash(f'Usuario {usuario.username} {estado} exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('usuarios.lista'))
