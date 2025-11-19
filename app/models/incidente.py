from app.extensions import db
from datetime import datetime

class Incidente(db.Model):
    __tablename__ = 'incidentes'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_incidente = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    codigo_trabajador = db.Column(db.String(50))
    dni = db.Column(db.String(8), nullable=False)
    nombre_usuario = db.Column(db.String(200), nullable=False)
    oficina = db.Column(db.String(200))
    sede = db.Column(db.String(50))
    tipo_incidente = db.Column(db.String(100), nullable=False)
    tipo_incidente_otro = db.Column(db.String(200))
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), nullable=False)
    personal_asignado = db.Column(db.Text)
    detalle_solucion = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    celular_encargado = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    registrado_por = db.Column(db.String(100))
    fecha_ultima_edicion = db.Column(db.DateTime)
    editado_por = db.Column(db.String(100))
    firma_path = db.Column(db.String(255))
    documento_path = db.Column(db.String(255))
    estado = db.Column(db.String(50), default='pendiente', nullable=False)
    
    historial = db.relationship('HistorialEdicion', backref='incidente', lazy='dynamic')
    
    @property
    def tipo_incidente_display(self):
        if self.tipo_incidente == 'Otro' and self.tipo_incidente_otro:
            return self.tipo_incidente_otro
        return self.tipo_incidente
    
    def __repr__(self):
        return f'<Incidente {self.id} - {self.tipo_incidente}>'
