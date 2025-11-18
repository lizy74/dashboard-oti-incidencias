from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Incidente, Practicante, Usuario
from app.extensions import db
from sqlalchemy import func
from datetime import date

bp = Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/')
@login_required
def index():
    if current_user.rol == 'admin':
        return dashboard_admin()
    elif current_user.rol == 'practicante':
        return dashboard_practicante()
    else:
        return redirect(url_for('auth.login'))


def dashboard_admin():
    total_incidentes = Incidente.query.count()
    prioridad_alta = Incidente.query.filter_by(prioridad='Alta').count()
    prioridad_media = Incidente.query.filter_by(prioridad='Media').count()
    prioridad_baja = Incidente.query.filter_by(prioridad='Baja').count()
    total_practicantes = Practicante.query.filter_by(activo=True).count()
    
    hoy = date.today()
    resueltos_hoy = Incidente.query.filter(
        func.date(Incidente.fecha_registro) == hoy
    ).count()
    
    # 🔧 CONTEO MEJORADO - Limpiar espacios extras
    practicantes = Practicante.query.filter_by(activo=True).all()
    incidentes_por_practicante = []
    
    for p in practicantes:
        count = 0
        # Limpiar espacios del nombre del practicante
        nombre_limpio = p.nombre_completo.strip()
        todos_incidentes = Incidente.query.all()
        
        for inc in todos_incidentes:
            if inc.personal_asignado:
                personal_str = str(inc.personal_asignado).strip()
                # Dividir por comas y limpiar espacios de CADA nombre
                nombres_asignados = [n.strip() for n in personal_str.split(',')]
                
                # Comparación case-insensitive y sin espacios
                for nombre in nombres_asignados:
                    if nombre_limpio.lower() == nombre.strip().lower():
                        count += 1
                        break  # Una vez por incidente
        
        if count > 0:
            incidentes_por_practicante.append({
                'nombre': p.nombre_completo.strip(),  # ← También limpiar aquí
                'total': count
            })
    
    incidentes_por_practicante.sort(key=lambda x: x['total'], reverse=True)
    
    ultimos_incidentes = Incidente.query.order_by(
        Incidente.fecha_registro.desc()
    ).limit(10).all()

    
    
    incidentes_por_tipo = db.session.query(
        Incidente.tipo_incidente,
        func.count(Incidente.id)
    ).group_by(Incidente.tipo_incidente).all()
    


    incidentes_por_sede = db.session.query(
        Incidente.sede,
        func.count(Incidente.id)
    ).group_by(Incidente.sede).all()
    
    return render_template('dashboard_admin.html',
        total_incidentes=total_incidentes,
        prioridad_alta=prioridad_alta,
        prioridad_media=prioridad_media,
        prioridad_baja=prioridad_baja,
        total_practicantes=total_practicantes,
        resueltos_hoy=resueltos_hoy,
        incidentes_por_practicante=incidentes_por_practicante,
        ultimos_incidentes=ultimos_incidentes,
        incidentes_por_tipo=incidentes_por_tipo,
        incidentes_por_sede=incidentes_por_sede
    )




def dashboard_practicante():
    nombre_practicante = current_user.nombre_completo.strip()
    todos_incidentes = Incidente.query.all()
    mis_incidentes = []

    for inc in todos_incidentes:
        if inc.personal_asignado:
            nombres_asignados = [n.strip() for n in str(inc.personal_asignado).split(',')]
            for nombre in nombres_asignados:
                if nombre_practicante.lower() == nombre.lower():
                    mis_incidentes.append(inc)
                    break

    total_mis_incidentes = len(mis_incidentes)
    total_resueltos = total_mis_incidentes

    mis_alta = len([i for i in mis_incidentes if i.prioridad == 'Alta'])
    mis_media = len([i for i in mis_incidentes if i.prioridad == 'Media'])
    mis_baja = len([i for i in mis_incidentes if i.prioridad == 'Baja'])

    mis_por_tipo = {}
    for incidente in mis_incidentes:
        tipo = incidente.tipo_incidente
        mis_por_tipo[tipo] = mis_por_tipo.get(tipo, 0) + 1

    ultimos_mis_incidentes = sorted(
        mis_incidentes,
        key=lambda x: x.fecha_registro,
        reverse=True
    )[:5]

    return render_template('dashboard_practicante.html',
        total_mis_incidentes=total_mis_incidentes,
        total_resueltos=total_resueltos,
        mis_alta=mis_alta,
        mis_media=mis_media,
        mis_baja=mis_baja,
        mis_por_tipo=mis_por_tipo,
        ultimos_mis_incidentes=ultimos_mis_incidentes
    )
