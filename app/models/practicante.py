from app.extensions import db
from datetime import datetime

class Practicante(db.Model):
    __tablename__ = 'practicantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    celular = db.Column(db.String(20))
    email = db.Column(db.String(200), unique=True)
    especialidad = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='practicante_info', uselist=False)
    
    @property
    def total_incidentes(self):
        from app.models.incidente import Incidente
        return Incidente.query.filter(
            Incidente.personal_asignado.contains(self.nombre_completo)
        ).count()
    
    def __repr__(self):
        return f'<Practicante {self.nombre_completo}>'
