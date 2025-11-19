from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.usuario import Usuario
from app.decorators import superadmin_required

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

@superadmin_bp.route('/administradores')
@login_required
@superadmin_required
def gestionar_administradores():
    """Lista todos los administradores"""
    administradores = Usuario.query.filter_by(rol='admin', activo=True).all()
    return render_template('superadmin/administradores.html', administradores=administradores)

@superadmin_bp.route('/administradores/crear', methods=['GET', 'POST'])
@login_required
@superadmin_required
def crear_administrador():
    """Crear nuevo administrador"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nombre_completo = request.form.get('nombre_completo')
        
        # Validar que no exista el usuario
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('superadmin.crear_administrador'))
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return redirect(url_for('superadmin.crear_administrador'))
        
        # Crear nuevo admin
        nuevo_admin = Usuario(
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            rol='admin',
            activo=True
        )
        nuevo_admin.set_password(password)
        
        db.session.add(nuevo_admin)
        db.session.commit()
        
        flash(f'Administrador {username} creado exitosamente', 'success')
        return redirect(url_for('superadmin.gestionar_administradores'))
    
    return render_template('superadmin/crear_admin.html')

@superadmin_bp.route('/administradores/editar/<int:admin_id>', methods=['GET', 'POST'])
@login_required
@superadmin_required
def editar_administrador(admin_id):
    """Editar administrador existente"""
    admin = Usuario.query.get_or_404(admin_id)
    
    # Verificar que sea un admin
    if admin.rol != 'admin':
        flash('Solo puedes editar administradores', 'danger')
        return redirect(url_for('superadmin.gestionar_administradores'))
    
    if request.method == 'POST':
        admin.nombre_completo = request.form.get('nombre_completo')
        admin.email = request.form.get('email')
        
        # Cambiar contraseña solo si se proporciona
        nueva_password = request.form.get('password')
        if nueva_password:
            admin.set_password(nueva_password)
        
        db.session.commit()
        flash(f'Administrador {admin.username} actualizado exitosamente', 'success')
        return redirect(url_for('superadmin.gestionar_administradores'))
    
    return render_template('superadmin/editar_admin.html', admin=admin)

@superadmin_bp.route('/administradores/eliminar/<int:admin_id>', methods=['POST'])
@login_required
@superadmin_required
def eliminar_administrador(admin_id):
    """Eliminar (desactivar) administrador"""
    admin = Usuario.query.get_or_404(admin_id)
    
    if admin.rol != 'admin':
        flash('Solo puedes eliminar administradores', 'danger')
        return redirect(url_for('superadmin.gestionar_administradores'))
    
    # Soft delete
    admin.activo = False
    db.session.commit()
    
    flash(f'Administrador {admin.username} eliminado exitosamente', 'success')
    return redirect(url_for('superadmin.gestionar_administradores'))
