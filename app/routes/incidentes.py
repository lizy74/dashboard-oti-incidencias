from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app.models import Incidente, Practicante, HistorialEdicion
from app.extensions import db
from app.config import Config
from datetime import datetime
from functools import wraps
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io


bp = Blueprint('incidentes', __name__, url_prefix='/incidentes')


def generar_pdf_bytes(incidente):
    """Genera PDF en bytes desde los datos del incidente"""
    
    # Buffer en memoria
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elementos = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=20,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    encabezado_style = ParagraphStyle(
        'Encabezado',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8
    )
    
    # Título
    titulo = Paragraph("ESCUELA DE TECNOLOGÍA INFORMÁTICA<br/>FORMATO REGISTRO DE INCIDENTES", titulo_style)
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    # Información básica en tabla
    info_basica = [
        ['N° ATENCIÓN', f"INC-2025-{incidente.id:03d}", 'FECHA INCIDENTE', incidente.fecha_incidente.strftime('%d/%m/%Y') if incidente.fecha_incidente else '', 'HORA', incidente.hora.strftime('%H:%M') if incidente.hora else ''],
    ]
    
    tabla_info = Table(info_basica, colWidths=[1.2*inch, 1.5*inch, 1.3*inch, 1.5*inch, 0.6*inch, 0.8*inch])
    tabla_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabla_info)
    elementos.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN 1: DATOS DEL USUARIO
    elementos.append(Paragraph("<b>1. DATOS DEL USUARIO</b>", styles['Heading3']))
    elementos.append(Spacer(1, 0.1*inch))
    
    datos_usuario = [
        ['CÓDIGO DE TRABAJADOR', incidente.codigo_trabajador or '', 'DNI', incidente.dni or ''],
        ['NOMBRE DE USUARIO', incidente.nombre_usuario or '', '', ''],
        ['OFICINA', incidente.oficina or '', 'SEDE', incidente.sede or ''],
    ]
    
    tabla_usuario = Table(datos_usuario, colWidths=[1.5*inch, 2*inch, 1.2*inch, 1.8*inch])
    tabla_usuario.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elementos.append(tabla_usuario)
    elementos.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN 2: INFORMACIÓN DEL INCIDENTE
    elementos.append(Paragraph("<b>2. INFORMACIÓN DEL INCIDENTE</b>", styles['Heading3']))
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph("<b>Tipo de Incidente:</b> " + (incidente.tipo_incidente or ''), encabezado_style))
    if incidente.tipo_incidente == 'Otro':
        elementos.append(Paragraph("<b>Especificar:</b> " + (incidente.tipo_incidente_otro or ''), encabezado_style))
    
    elementos.append(Spacer(1, 0.1*inch))
    elementos.append(Paragraph("<b>Descripción Detallada:</b>", styles['Heading4']))
    elementos.append(Paragraph(incidente.descripcion or 'Sin descripción', encabezado_style))
    
    elementos.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN 3: DATOS DEL PERSONAL ASIGNADO
    elementos.append(Paragraph("<b>3. DATOS DEL PERSONAL ASIGNADO</b>", styles['Heading3']))
    elementos.append(Spacer(1, 0.1*inch))
    
    datos_personal = [
        ['PERSONAL ASIGNADO', incidente.personal_asignado or 'Sin asignar', 'PRIORIDAD', incidente.prioridad or ''],
    ]
    
    tabla_personal = Table(datos_personal, colWidths=[2.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    tabla_personal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabla_personal)
    elementos.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN 4: DATOS DE RESOLUCIÓN
    elementos.append(Paragraph("<b>4. DATOS DE RESOLUCIÓN</b>", styles['Heading3']))
    elementos.append(Spacer(1, 0.1*inch))
    
    elementos.append(Paragraph("<b>Detalle de Actividad Realizada:</b>", styles['Heading4']))
    elementos.append(Paragraph(incidente.detalle_solucion or 'Sin detalles', encabezado_style))
    
    elementos.append(Spacer(1, 0.1*inch))
    elementos.append(Paragraph("<b>Comentarios y Observaciones:</b>", styles['Heading4']))
    elementos.append(Paragraph(incidente.observaciones or 'Sin observaciones', encabezado_style))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    fecha_generacion = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    elementos.append(Paragraph(f"<i>Reporte generado el {fecha_generacion}</i>", styles['Normal']))
    
    if incidente.celular_encargado:
        elementos.append(Paragraph(f"<i>Celular encargado: {incidente.celular_encargado}</i>", styles['Normal']))
    
    # Construir PDF
    doc.build(elementos)
    
    buffer.seek(0)
    return buffer.getvalue()


@bp.route('/preview-pdf/<int:id>')
@login_required
def preview_pdf(id):
    """Muestra vista previa del PDF en el navegador"""
    incidente = Incidente.query.get_or_404(id)
    
    pdf_bytes = generar_pdf_bytes(incidente)
    
    buffer = io.BytesIO(pdf_bytes)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=False
    )


@bp.route('/descargar-pdf/<int:id>')
@login_required
def descargar_pdf(id):
    """Descarga el PDF"""
    incidente = Incidente.query.get_or_404(id)
    
    pdf_bytes = generar_pdf_bytes(incidente)
    
    buffer = io.BytesIO(pdf_bytes)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'incidente_{incidente.id}.pdf'
    )


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rol != 'admin':
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
def lista():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', '')
    prioridad = request.args.get('prioridad', '')
    tipo = request.args.get('tipo', '')
    practicante_id = request.args.get('practicante_id', '')
    
    if current_user.rol in ['admin', 'superadmin']:
        query = Incidente.query
    else:
        query = Incidente.query.filter(
            Incidente.personal_asignado.contains(current_user.nombre_completo)
        )
    
    if busqueda:
        query = query.filter(
            db.or_(
                Incidente.descripcion.contains(busqueda),
                Incidente.nombre_usuario.contains(busqueda),
                Incidente.oficina.contains(busqueda),
                Incidente.dni.contains(busqueda)
            )
        )
    
    if prioridad:
        query = query.filter_by(prioridad=prioridad)
    
    if tipo:
        query = query.filter_by(tipo_incidente=tipo)
    
    if practicante_id:
        practicante = Practicante.query.get(practicante_id)
        if practicante:
            query = query.filter(Incidente.personal_asignado.contains(practicante.nombre_completo))
    
    incidentes = query.order_by(Incidente.id.desc()).paginate(
        page=page,
        per_page=Config.INCIDENTES_POR_PAGINA,
        error_out=False
    )
    
    practicantes = Practicante.query.filter_by(activo=True).order_by(Practicante.nombre_completo).all()
    
    return render_template('incidentes_lista.html',
        incidentes=incidentes,
        busqueda=busqueda,
        prioridad=prioridad,
        tipo=tipo,
        practicante_id=practicante_id,
        practicantes=practicantes,
        tipos_incidente=Config.TIPOS_INCIDENTE,
        sedes=Config.SEDES,
        prioridades=Config.PRIORIDADES
    )


# Mantén el resto de tus funciones (nuevo, detalle, editar, eliminar)...
@bp.route('/ver-pdf/<int:id>')
@login_required
def ver_pdf(id):
    """Muestra la plantilla HTML lista para imprimir a PDF"""
    incidente = Incidente.query.get_or_404(id)
    
    data = {
        'n_atencion': f"INC-2025-{incidente.id:03d}",
        'fecha_incidente': incidente.fecha_incidente.strftime('%d/%m/%Y') if incidente.fecha_incidente else '',
        'hora': incidente.hora.strftime('%H:%M') if incidente.hora else '',
        'codigo_trabajador': incidente.codigo_trabajador or '',
        'dni': incidente.dni or '',
        'nombre_usuario': incidente.nombre_usuario or '',
        'oficina': incidente.oficina or '',
        'sede': incidente.sede or '',
        'tipo_incidente': incidente.tipo_incidente or '',
        'tipo_incidente_otro': incidente.tipo_incidente_otro or '',
        'descripcion': incidente.descripcion or '',
        'personal_asignado': incidente.personal_asignado or '',
        'prioridad': incidente.prioridad or '',
        'detalle_solucion': incidente.detalle_solucion or '',
        'observaciones': incidente.observaciones or '',
        'celular_encargado': incidente.celular_encargado or '',
    }
    
    return render_template('pdf_incidente_plantilla.html', **data)




@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        try:
            # Obtener fecha y hora del formulario
            fecha_str = request.form.get('fecha_incidente')
            hora_str = request.form.get('hora')
            
            if not fecha_str or not hora_str:
                flash('Fecha y hora son obligatorias.', 'error')
                return redirect(url_for('incidentes.nuevo'))
            
            fecha_incidente = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora = datetime.strptime(hora_str, '%H:%M').time()
            
            # Obtener multiple asignados
            personal_ids = request.form.getlist('personal_asignado')
            
            # Convertir IDs a nombres
            personal_nombres = []
            for pid in personal_ids:
                practicante = Practicante.query.get(pid)
                if practicante:
                    personal_nombres.append(practicante.nombre_completo)
            personal_asignado = ', '.join(personal_nombres) if personal_nombres else ''
            
            incidente = Incidente(
                fecha_incidente=fecha_incidente,
                hora=hora,
                codigo_trabajador=request.form.get('codigo_trabajador', ''),
                dni=request.form.get('dni', ''),
                nombre_usuario=request.form.get('nombre_usuario', ''),
                oficina=request.form.get('oficina', ''),
                sede=request.form.get('sede', ''),
                tipo_incidente=request.form.get('tipo_incidente', ''),
                tipo_incidente_otro=request.form.get('tipo_incidente_otro', ''),
                descripcion=request.form.get('descripcion', ''),
                prioridad=request.form.get('prioridad', ''),
                personal_asignado=personal_asignado,
                detalle_solucion=request.form.get('detalle_solucion', ''),
                observaciones=request.form.get('observaciones', ''),
                celular_encargado=request.form.get('celular_encargado', ''),
                fecha_registro=datetime.now(),
                registrado_por=current_user.nombre_completo
            )
            
            db.session.add(incidente)
            db.session.commit()
            flash('✅ Incidente registrado exitosamente', 'success')
            return redirect(url_for('incidentes.lista'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {str(e)}', 'error')
    
    practicantes = Practicante.query.filter_by(activo=True).all()
    
    return render_template('incidente_nuevo.html', 
                          practicantes=practicantes,
                          tipos_incidente=Config.TIPOS_INCIDENTE,
                          sedes=Config.SEDES,
                          prioridades=Config.PRIORIDADES)




@bp.route('/<int:id>')
@login_required
def detalle(id):
    incidente = Incidente.query.get_or_404(id)
    
    if current_user.rol == 'practicante':
        if not incidente.personal_asignado or current_user.nombre_completo not in incidente.personal_asignado:
            flash('No tienes permiso para ver este incidente', 'error')
            return redirect(url_for('incidentes.lista'))
    
    historial = HistorialEdicion.query.filter_by(
        incidente_id=id
    ).order_by(HistorialEdicion.fecha_edicion.desc()).all()
    
    return render_template('incidente_detalle.html',
        incidente=incidente,
        historial=historial
    )

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    incidente = Incidente.query.get_or_404(id)
    
    if current_user.rol == 'practicante':
        if not incidente.personal_asignado or current_user.nombre_completo not in incidente.personal_asignado:
            flash('No tienes permiso para editar este incidente', 'error')
            return redirect(url_for('incidentes.lista'))
    
    if request.method == 'POST':
        try:
            campos_restringidos = ['personal_asignado'] if current_user.rol == 'practicante' else []
            
            fecha_str = request.form.get('fecha_incidente')
            hora_str = request.form.get('hora')
            
            nueva_fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            nueva_hora = datetime.strptime(hora_str, '%H:%M').time()
            
            cambios = []
            
            if incidente.fecha_incidente != nueva_fecha:
                cambios.append(('fecha_incidente', str(incidente.fecha_incidente), str(nueva_fecha)))
                incidente.fecha_incidente = nueva_fecha
            
            if incidente.hora != nueva_hora:
                cambios.append(('hora', str(incidente.hora), str(nueva_hora)))
                incidente.hora = nueva_hora
            
            campos_texto = [
                'codigo_trabajador', 'dni', 'nombre_usuario', 'oficina', 'sede',
                'tipo_incidente', 'descripcion', 'prioridad', 'detalle_solucion',
                'observaciones', 'celular_encargado'
            ]
            
            for campo in campos_texto:
                if campo in campos_restringidos:
                    continue
                
                valor_nuevo = request.form.get(campo, '')
                valor_anterior = getattr(incidente, campo) or ''
                
                if str(valor_anterior) != str(valor_nuevo):
                    cambios.append((campo, str(valor_anterior), str(valor_nuevo)))
                    setattr(incidente, campo, valor_nuevo)
            
            if incidente.tipo_incidente == 'Otro':
                tipo_otro = request.form.get('tipo_incidente_otro')
                if incidente.tipo_incidente_otro != tipo_otro:
                    cambios.append(('tipo_incidente_otro', incidente.tipo_incidente_otro or '', tipo_otro))
                    incidente.tipo_incidente_otro = tipo_otro
            
            if current_user.rol in ['admin', 'superadmin']:
                personal_ids = request.form.getlist('personal_asignado')
                personal_nombres = []
                for pid in personal_ids:
                    practicante = Practicante.query.get(pid)
                    if practicante:
                        personal_nombres.append(practicante.nombre_completo)
                
                nuevo_personal = ', '.join(personal_nombres) if personal_nombres else None
                if incidente.personal_asignado != nuevo_personal:
                    cambios.append(('personal_asignado', incidente.personal_asignado or '', nuevo_personal or ''))
                    incidente.personal_asignado = nuevo_personal
            
            incidente.fecha_ultima_edicion = datetime.utcnow()
            incidente.editado_por = current_user.nombre_completo
            
            for campo, valor_ant, valor_nue in cambios:
                historial = HistorialEdicion(
                    incidente_id=incidente.id,
                    usuario_id=current_user.id,
                    accion='Editado',
                    campo_editado=campo,
                    valor_anterior=valor_ant,
                    valor_nuevo=valor_nue
                )
                db.session.add(historial)
            
            db.session.commit()
            
            flash(f'Incidente actualizado exitosamente. {len(cambios)} cambios registrados.', 'success')
            return redirect(url_for('incidentes.detalle', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    practicantes = Practicante.query.filter_by(activo=True).order_by(Practicante.nombre_completo).all()
    
    practicantes_asignados = []
    if incidente.personal_asignado:
        nombres_asignados = [n.strip() for n in incidente.personal_asignado.split(',')]
        practicantes_asignados = [p.id for p in practicantes if p.nombre_completo in nombres_asignados]
    
    return render_template('incidente_editar.html',
        incidente=incidente,
        practicantes=practicantes,
        practicantes_asignados=practicantes_asignados,
        tipos_incidente=Config.TIPOS_INCIDENTE,
        sedes=Config.SEDES,
        prioridades=Config.PRIORIDADES,
        puede_editar_personal=current_user.rol == 'admin'
    )

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar(id):
    try:
        incidente = Incidente.query.get_or_404(id)
        
        historial = HistorialEdicion(
            incidente_id=incidente.id,
            usuario_id=current_user.id,
            accion='Eliminado',
            campo_editado='Incidente completo',
            valor_anterior=f'Incidente #{incidente.id}'
        )
        db.session.add(historial)
        
        db.session.delete(incidente)
        db.session.commit()
        
        flash('Incidente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('incidentes.lista'))
