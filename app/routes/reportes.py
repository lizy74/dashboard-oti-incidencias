from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from app.models import Incidente, Practicante
from app.extensions import db
from app.config import Config
from app.decorators import admin_required  # IMPORTAR EL CORRECTO
import pandas as pd
from io import BytesIO
from datetime import datetime


bp = Blueprint('reportes', __name__, url_prefix='/reportes')


@bp.route('/')
@login_required
@admin_required  # Ahora permite admin y superadmin
def index():
    practicantes = Practicante.query.filter_by(activo=True).all()
    return render_template('reportes.html',
        es_admin=True,
        practicantes=practicantes,
        tipos=Config.TIPOS_INCIDENTE,
        sedes=Config.SEDES,
        prioridades=Config.PRIORIDADES
    )


@bp.route('/generar', methods=['POST'])
@login_required
@admin_required
def generar():
    try:
        tipo_reporte = request.form.get('tipo_reporte')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        practicante_id = request.form.get('practicante_id')
        prioridad = request.form.get('prioridad')
        sede = request.form.get('sede')
        
        query = Incidente.query
        
        if fecha_inicio:
            query = query.filter(Incidente.fecha_incidente >= datetime.strptime(fecha_inicio, '%Y-%m-%d').date())
        
        if fecha_fin:
            query = query.filter(Incidente.fecha_incidente <= datetime.strptime(fecha_fin, '%Y-%m-%d').date())
        
        if practicante_id:
            practicante = Practicante.query.get(practicante_id)
            if practicante:
                query = query.filter(Incidente.personal_asignado.contains(practicante.nombre_completo))
        
        if prioridad:
            query = query.filter_by(prioridad=prioridad)
        
        if sede:
            query = query.filter_by(sede=sede)
        
        incidentes = query.order_by(Incidente.fecha_registro.desc()).all()
        
        data = []
        for idx, inc in enumerate(incidentes, 1):
            data.append({
                'N° Atencion': idx,
                'Fecha del Incidente': inc.fecha_incidente.strftime('%d/%m/%Y'),
                'Hora': inc.hora.strftime('%H:%M'),
                'Codigo del Trabajador': inc.codigo_trabajador or '',
                'DNI': inc.dni,
                'Nombre de Usuario': inc.nombre_usuario,
                'Oficina': inc.oficina or '',
                'Sede': inc.sede or '',
                'Tipo de Incidente': inc.tipo_incidente_display,
                'Descripcion del Incidente': inc.descripcion,
                'Personal Asignado': inc.personal_asignado or '',
                'Prioridad': inc.prioridad,
                'Detalles de Solucion': inc.detalle_solucion or '',
                'Observacion y Comentarios': inc.observaciones or '',
                'Celular de Encargado': inc.celular_encargado or ''
            })
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Incidentes')
        output.seek(0)
        
        filename = f'reporte_incidentes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return f'Error al generar reporte: {str(e)}', 500
