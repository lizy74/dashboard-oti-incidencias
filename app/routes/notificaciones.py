from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Notificacion
from app.extensions import db

bp = Blueprint('notificaciones', __name__, url_prefix='/notificaciones')

@bp.route('/')
@login_required
def lista():
    notificaciones = Notificacion.query.filter_by(usuario_id=current_user.id).order_by(Notificacion.fecha_creacion.desc()).all()
    return render_template('notificaciones/lista.html', notificaciones=notificaciones)

@bp.route('/marcar_leida/<int:id>')
@login_required
def marcar_leida(id):
    notificacion = Notificacion.query.get_or_404(id)
    if notificacion.usuario_id != current_user.id:
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('notificaciones.lista'))

    notificacion.leido = True
    db.session.commit()
    return redirect(url_for('notificaciones.lista'))
