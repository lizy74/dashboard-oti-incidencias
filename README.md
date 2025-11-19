# 📋 Sistema de Gestión de Incidencias SURC-OTI

Sistema web desarrollado para la gestión integral de incidencias técnicas del área de Oficina de Tecnologías de la Información (OTI) de la Universidad Nacional del Altiplano de Puno.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-UNAP-orange.svg)

## 🌟 Características Principales

### Gestión de Incidentes
- ✅ Registro detallado de incidencias técnicas
- ✅ Asignación de prioridad (Alta, Media, Baja)
- ✅ Seguimiento de estado en tiempo real
- ✅ Historial completo de ediciones
- ✅ Adjuntar información del solicitante y encargado

### Sistema de Usuarios
- 👑 **Super Administrador**: Control total del sistema  
- 🛡️ **Administrador**: Gestión de incidentes y usuarios  
- 👤 **Practicante**: Registro y resolución de incidentes  

### Dashboard Analítico
- 📊 Estadísticas en tiempo real  
- 📈 Gráficos interactivos con Chart.js  
- 🎯 Métricas por prioridad, tipo y practicante  
- ⏱️ Incidentes resueltos por período  

### Reportes
- 📄 Exportación a PDF con formato profesional  
- 📊 Exportación a Excel para análisis  
- 🔍 Filtros avanzados por fecha, prioridad, tipo  

### Interfaz Moderna
- 📱 Diseño 100% responsive  
- 🎨 UI moderna con TailwindCSS y DaisyUI  
- 🌙 Tema claro optimizado  
- ⚡ Carga rápida y optimizada  

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework:** Flask 3.0.0  
- **ORM:** SQLAlchemy 2.0.44  
- **Autenticación:** Flask-Login 0.6.3  
- **Base de Datos:** SQLite (migrable a PostgreSQL/MySQL)

### Frontend
- **CSS Framework:** TailwindCSS 3.x  
- **UI Components:** DaisyUI 3.9.4  
- **Iconos:** Material Design Icons 7.4.47  
- **Gráficos:** Chart.js  

### Reportes
- **PDF:** ReportLab 4.4.4  
- **Excel:** OpenPyXL 3.1.5  
- **Análisis:** Pandas 2.3.3  

---

## 📋 Requisitos Previos

- Python 3.9 o superior  
- pip (gestor de paquetes de Python)  
- Git (para clonar el repositorio)  

### Verificar instalación de Python:
```bash
python --version
```

Debe mostrar: Python 3.9.x o superior

---

## 🚀 Instalación Rápida (con Base de Datos Existente)

1. **Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/dashboard-oti-incidencias.git
cd dashboard-oti-incidencias
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**Linux/Mac**
```bash
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Crear carpeta instance**
```bash
mkdir instance
```

5. **Copiar base de datos existente**

**Windows**
```bash
copy ruta\a\tu\incidencias.db instance\incidencias.db
```

**Linux/Mac**
```bash
cp ruta/a/tu/incidencias.db instance/incidencias.db
```

6. **Ejecutar el sistema**
```bash
python run.py
```

**Acceder al sistema:**  
http://localhost:5000  

⚠️ **Importante:**  
- NO ejecutar `db.create_all()`  
- NO ejecutar `crear_superadmin.py`  
- Solo copiar la BD y ejecutar  

---

## 🆕 Instalación desde Cero (Sin Base de Datos)

<details>
<summary>Click para expandir</summary>

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/dashboard-oti-incidencias.git
cd dashboard-oti-incidencias
```

### 2️⃣ Crear Entorno Virtual

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Crear Base de Datos
```bash
mkdir instance
python
```

Dentro de Python:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

### 5️⃣ Crear Super Administrador
```bash
python crear_superadmin.py
```

### 6️⃣ Ejecutar
```bash
python run.py
```

</details>

---

## 👥 Roles y Permisos

| Rol | Crear Incidentes | Ver Todos | Gestionar Usuarios | Gestionar Admins | Reportes |
|-----|------------------|-----------|-------------------|------------------|----------|
| **Super Admin** 👑 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Admin** 🛡️ | ✅ | ✅ | ✅ (Solo Practicantes) | ❌ | ✅ |
| **Practicante** 👤 | ✅ | ⚠️ (Solo asignados) | ❌ | ❌ | ❌ |

---

## 📁 Estructura del Proyecto
```
dashboard-oti-incidencias/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
│
├── instance/
│   └── incidencias.db
│
├── config.py
├── crear_superadmin.py
├── requirements.txt
├── run.py
└── README.md
```

---

## 🔒 Seguridad

- Contraseñas hasheadas (PBKDF2)  
- Protección CSRF  
- Control de acceso basado en roles  
- Sesiones seguras con Flask-Login  
- Validación de datos  
- Protección XSS  

---

## 🐛 Solución de Problemas

### Error: “No module named 'flask'”
```bash
venv\Scripts\activate
```

### Puerto 5000 ocupado
```python
app.run(port=8080)
```

### Base de datos no encontrada
```bash
dir instance\
```

---

## 📝 Licencia

Proyecto desarrollado para la **Universidad Nacional del Altiplano de Puno**, Oficina de Tecnologías de la Información.

---

## 👨‍💻 Desarrollo

- **Año:** 2025  
- **Versión:** 1.0.0

---

## 📞 Soporte

- Issues: GitHub  
- Email: oti@unap.edu.pe

---

**⭐ Si este proyecto te fue útil, dale una estrella en GitHub ⭐**
