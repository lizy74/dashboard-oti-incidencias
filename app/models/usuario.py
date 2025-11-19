from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(200))
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    practicante_id = db.Column(db.Integer, db.ForeignKey('practicantes.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
    
    def es_superadmin(self):
        """Verifica si el usuario es super administrador"""
        return self.rol == 'superadmin'

    def es_admin(self):
        """Verifica si el usuario es administrador (incluye superadmin)"""
        return self.rol in ['admin', 'superadmin']

    def es_practicante(self):
        """Verifica si el usuario es practicante"""
        return self.rol == 'practicante'

    def puede_gestionar_admins(self):
        """Solo superadmin puede gestionar administradores"""
        return self.rol == 'superadmin'

    def es_solicitante(self):
        """Verifica si el usuario es solicitante"""
        return self.rol == 'solicitante'
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
