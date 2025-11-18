from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, migrate
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import auth, dashboard, incidentes, reportes, importar, practicantes, usuarios
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(incidentes.bp)
    app.register_blueprint(reportes.bp)
    app.register_blueprint(importar.bp)
    app.register_blueprint(practicantes.bp)
    app.register_blueprint(usuarios.bp)
    
    with app.app_context():
        db.create_all()
        crear_admin()
    
    @app.template_filter('fecha_es')
    def fecha_es_filter(fecha):
        if fecha:
            return fecha.strftime('%d/%m/%Y')
        return ''
    
    @app.template_filter('hora_es')
    def hora_es_filter(hora):
        if hora:
            return hora.strftime('%H:%M')
        return ''
    
    return app

def crear_admin():
    from app.models import Usuario
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            email='admin@unap.edu.pe',
            nombre_completo='Administrador del Sistema',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado - username: admin, password: admin123")
