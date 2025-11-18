from app.extensions import db
from datetime import datetime

class HistorialEdicion(db.Model):
    __tablename__ = 'historial_ediciones'
    
    id = db.Column(db.Integer, primary_key=True)
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes.id'), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # ← CAMBIAR A TRUE


    fecha_edicion = db.Column(db.DateTime, default=datetime.utcnow)
    campo_editado = db.Column(db.String(100))
    valor_anterior = db.Column(db.Text)
    valor_nuevo = db.Column(db.Text)
    accion = db.Column(db.String(50))
    
    usuario = db.relationship('Usuario', backref='ediciones_realizadas')
    
    def __repr__(self):
        return f'<HistorialEdicion {self.accion} - Incidente #{self.incidente_id}>'
