from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Incidente, Practicante
from app.extensions import db
import pandas as pd
from datetime import datetime
from functools import wraps

bp = Blueprint('importar', __name__, url_prefix='/importar')

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
def index():
    return render_template('importar.html')


@bp.route('/csv', methods=['POST'])
@login_required
@admin_required
def importar_csv():
    try:
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('importar.index'))

        archivo = request.files['archivo']

        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('importar.index'))

        if not archivo.filename.endswith('.csv'):
            flash('El archivo debe ser CSV', 'error')
            return redirect(url_for('importar.index'))

        df = pd.read_csv(archivo)

        columnas_requeridas = ['Fecha del Incidente', 'Hora', 'DNI', 'Nombre de Usuario', 'Tipo de Incidente', 'Descripcion del Incidente', 'Prioridad']

        for col in columnas_requeridas:
            if col not in df.columns:
                flash(f'Falta la columna requerida: {col}', 'error')
                return redirect(url_for('importar.index'))

        importados = 0
        errores = 0

        # Diccionario para normalizar todos los tipos posibles a solo 4 categorías
        tipos_map = {
            "internet": "Internet",
            "hardware": "Hardware",
            "software": "Software",
            "otro": "Otro"
        }

        for idx, row in df.iterrows():
            try:
                fecha_str = str(row['Fecha del Incidente'])
                hora_str = str(row['Hora'])

                if '/' in fecha_str:
                    fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
                else:
                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

                if ':' in hora_str:
                    hora = datetime.strptime(hora_str, '%H:%M').time()
                else:
                    hora = datetime.strptime('00:00', '%H:%M').time()

                # Normaliza el tipo de incidente
                tipo_original = str(row.get('Tipo de Incidente', 'Otro')).strip().lower()
                tipo_normalizado = tipos_map.get(tipo_original, "Otro")

                incidente = Incidente(
                    fecha_incidente=fecha,
                    hora=hora,
                    codigo_trabajador=str(row.get('Codigo del Trabajador', '')),
                    dni=str(row['DNI']),
                    nombre_usuario=str(row['Nombre de Usuario']),
                    oficina=str(row.get('Oficina', '')),
                    sede=str(row.get('Sede', '')),
                    tipo_incidente=tipo_normalizado,
                    descripcion=str(row['Descripcion del Incidente']),
                    personal_asignado=str(row.get('Personal Asignado', '')),
                    prioridad=str(row['Prioridad']),
                    detalle_solucion=str(row.get('Detalles de Solucion', '')),
                    observaciones=str(row.get('Observacion y Comentarios', '')),
                    celular_encargado=str(row.get('Celular de Encargado', '')),
                    registrado_por=f'{current_user.nombre_completo} (Importado)'
                )
                db.session.add(incidente)
                importados += 1

            except Exception as e:
                errores += 1
                print(f'Error en fila {idx + 2}: {str(e)}')
                continue

        db.session.commit()
        flash(f'Importación completada: {importados} incidentes importados, {errores} errores', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar: {str(e)}', 'error')

    return redirect(url_for('importar.index'))
