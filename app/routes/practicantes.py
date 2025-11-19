from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Practicante, Usuario
from app.extensions import db
from app.config import Config
from app.decorators import admin_required  # Usar el decorador correcto


bp = Blueprint('practicantes', __name__, url_prefix='/practicantes')


@bp.route('/lista')
@login_required
@admin_required
def lista():
    practicantes = Practicante.query.order_by(Practicante.nombre_completo).all()
    return render_template('practicantes.html',
        practicantes=practicantes,
        especialidades=Config.ESPECIALIDADES
    )


@bp.route('/crear', methods=['POST'])
@login_required
@admin_required
def crear():
    try:
        nombre_completo = request.form.get('nombre_completo')
        celular = request.form.get('celular')
        email = request.form.get('email')
        especialidad = request.form.get('especialidad')
        
        if Practicante.query.filter_by(email=email).first():
            flash('Ya existe un practicante con ese email', 'error')
            return redirect(url_for('practicantes.lista'))
        
        practicante = Practicante(
            nombre_completo=nombre_completo,
            celular=celular,
            email=email,
            especialidad=especialidad,
            activo=True
        )
        
        db.session.add(practicante)
        db.session.flush()
        
        username = email.split('@')[0]
        contador = 1
        username_base = username
        while Usuario.query.filter_by(username=username).first():
            username = f"{username_base}{contador}"
            contador += 1
        
        usuario = Usuario(
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            rol='practicante',
            practicante_id=practicante.id
        )
        usuario.set_password(username)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(f'Practicante creado exitosamente. Usuario: {username}, Contraseña: {username}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear practicante: {str(e)}', 'error')
    
    return redirect(url_for('practicantes.lista'))


@bp.route('/editar/<int:id>', methods=['POST'])
@login_required
@admin_required
def editar(id):
    try:
        practicante = Practicante.query.get_or_404(id)
        
        practicante.nombre_completo = request.form.get('nombre_completo')
        practicante.celular = request.form.get('celular')
        practicante.email = request.form.get('email')
        practicante.especialidad = request.form.get('especialidad')
        
        if practicante.usuario:
            practicante.usuario.nombre_completo = practicante.nombre_completo
            practicante.usuario.email = practicante.email
        
        db.session.commit()
        flash('Practicante actualizado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar: {str(e)}', 'error')
    
    return redirect(url_for('practicantes.lista'))


@bp.route('/toggle/<int:id>', methods=['POST'])
@login_required
@admin_required
def toggle_estado(id):
    try:
        practicante = Practicante.query.get_or_404(id)
        practicante.activo = not practicante.activo
        
        if practicante.usuario:
            practicante.usuario.activo = practicante.activo
        
        db.session.commit()
        estado = 'activado' if practicante.activo else 'desactivado'
        flash(f'Practicante {estado} exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('practicantes.lista'))


@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    try:
        practicante = Practicante.query.get_or_404(id)
        nombre_practicante = practicante.nombre_completo
        
        if practicante.usuario:
            usuario_id = practicante.usuario.id
            
            from app.models.historial import HistorialEdicion
            HistorialEdicion.query.filter_by(usuario_id=usuario_id).update(
                {'usuario_id': None},
                synchronize_session=False
            )
        
            db.session.delete(practicante.usuario)

        db.session.delete(practicante)
        db.session.commit()
        
        flash(f'✅ Practicante "{nombre_practicante}" eliminado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error al eliminar: {str(e)}', 'error')
        print(f"Error en eliminar practicante: {str(e)}")
    
    return redirect(url_for('practicantes.lista'))
