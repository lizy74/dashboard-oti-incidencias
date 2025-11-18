from app import create_app, db
from app.models import Incidente, Practicante

app = create_app()
with app.app_context():
    practicantes = Practicante.query.filter_by(activo=True).all()
    todos_incidentes = Incidente.query.all()

    print("\n### Conteo de incidentes por practicante ###\n")
    for p in practicantes:
        count = 0
        nombre_limpio = p.nombre_completo.strip()
        for inc in todos_incidentes:
            if inc.personal_asignado:
                nombres_asignados = [n.strip() for n in str(inc.personal_asignado).strip().split(',')]
                for nombre in nombres_asignados:
                    if nombre_limpio.lower() == nombre.lower():
                        count += 1
                        break
        print(f"{nombre_limpio} : {count} incidentes")
