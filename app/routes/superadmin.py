from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.usuario import Usuario
from app.models.incidente import Incidente
from app.models.practicante import Practicante
from app.models.notificacion import Notificacion
from app.decorators import superadmin_required

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

@superadmin_bp.route('/panel_asignacion')
@login_required
@superadmin_required
def panel_asignacion():
    incidentes = Incidente.query.order_by(Incidente.fecha_registro.desc()).all()
    practicantes = Practicante.query.filter_by(activo=True).all()

    # Pre-calcular los IDs de los practicantes asignados a cada incidente
    for incidente in incidentes:
        nombres_asignados = [nombre.strip() for nombre in incidente.personal_asignado.split(',') if nombre]
        practicantes_asignados = Practicante.query.filter(Practicante.nombre_completo.in_(nombres_asignados)).all()
        incidente.practicantes_asignados_ids = {p.id for p in practicantes_asignados}

    return render_template('superadmin/panel.html', incidentes=incidentes, practicantes=practicantes)

@superadmin_bp.route('/asignar/<int:id>', methods=['POST'])
@login_required
@superadmin_required
def asignar(id):
    incidente = Incidente.query.get_or_404(id)

    estado = request.form.get('estado')
    practicantes_ids = request.form.getlist('practicantes')
    comentario = request.form.get('comentario', '').strip()

    if estado:
        incidente.estado = estado

    if practicantes_ids:
        practicantes_asignados = []
        for pid in practicantes_ids:
            practicante = Practicante.query.get(pid)
            if practicante:
                practicantes_asignados.append(practicante)

        incidente.personal_asignado = ', '.join([p.nombre_completo for p in practicantes_asignados])

        # Enviar notificaciones
        for practicante in practicantes_asignados:
            if practicante.usuario:
                mensaje = f"Se te ha asignado la incidencia #{incidente.id}."
                if comentario:
                    mensaje += f" Comentario del admin: '{comentario}'"

                notificacion = Notificacion(
                    usuario_id=practicante.usuario.id,
                    mensaje=mensaje
                )
                db.session.add(notificacion)
    else:
        incidente.personal_asignado = ''

    db.session.commit()
    flash('Incidente actualizado correctamente.', 'success')
    return redirect(url_for('superadmin.panel_asignacion'))

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
