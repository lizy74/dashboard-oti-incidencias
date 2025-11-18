import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'incidencias.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    TIPOS_INCIDENTE = ['Internet', 'Software', 'Hardware', 'Otro']
    SEDES = ['C.U.', 'Ed. Cont.', 'Otro']
    PRIORIDADES = ['Baja', 'Media', 'Alta']
    ESPECIALIDADES = [
        'Redes y Comunicaciones',
        'Soporte Técnico',
        'Desarrollo Web',
        'Gobierno Electrónico',
        'General'
    ]
    
    INCIDENTES_POR_PAGINA = 12
