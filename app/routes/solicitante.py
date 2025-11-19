from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import RegistrationForm, SolicitanteIncidenteForm
from app.models import Usuario, Incidente
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from uuid import uuid4

bp = Blueprint('solicitante', __name__, url_prefix='/solicitante')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(
            username=form.username.data,
            email=form.email.data,
            nombre_completo=form.nombre_completo.data,
            rol='solicitante'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('solicitante/register.html', form=form)

@bp.route('/portal')
@login_required
def portal():
    if current_user.rol != 'solicitante':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('dashboard.index'))

    incidentes = Incidente.query.filter_by(registrado_por=current_user.nombre_completo).order_by(Incidente.fecha_registro.desc()).all()
    return render_template('solicitante/portal.html', incidentes=incidentes)

@bp.route('/crear_incidente', methods=['GET', 'POST'])
@login_required
def crear_incidente():
    if current_user.rol != 'solicitante':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = SolicitanteIncidenteForm()
    if form.validate_on_submit():
        documento_path = None
        if form.documento.data:
            try:
                documentos_dir = os.path.join('app', 'static', 'documentos')
                os.makedirs(documentos_dir, exist_ok=True)

                f = form.documento.data
                filename = secure_filename(f.filename)
                unique_filename = f"{uuid4().hex}_{filename}"
                filepath = os.path.join(documentos_dir, unique_filename)
                f.save(filepath)
                documento_path = os.path.join('documentos', unique_filename).replace('\\', '/')
            except Exception as e:
                flash(f'Error al guardar el documento: {str(e)}', 'danger')
                return redirect(url_for('solicitante.crear_incidente'))

        incidente = Incidente(
            nombre_usuario=current_user.nombre_completo,
            dni=current_user.username, # Asumiendo que el DNI se guarda en username para solicitantes
            descripcion=form.descripcion.data,
            tipo_incidente=form.titulo.data, # Usamos el título como tipo de incidente simplificado
            registrado_por=current_user.nombre_completo,
            documento_path=documento_path,
            # Valores por defecto para campos no presentes en el form simplificado
            fecha_incidente=db.func.current_date(),
            hora=db.func.current_time(),
            prioridad='Media',
            sede='C.U.'
        )
        db.session.add(incidente)
        db.session.commit()
        flash('Incidente enviado correctamente.', 'success')
        return redirect(url_for('solicitante.portal'))

    return render_template('solicitante/crear_incidente.html', form=form)
