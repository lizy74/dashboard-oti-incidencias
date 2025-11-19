# Documentación del Sistema de Gestión de Incidencias SURC-OTI

## 1. Descripción General

Este documento proporciona una descripción completa del Sistema de Gestión de Incidencias SURC-OTI, una aplicación web diseñada para la Oficina de Tecnologías de la Información (OTI) de la Universidad Nacional del Altiplano de Puno. El sistema facilita el registro, seguimiento y gestión de incidencias técnicas, optimizando los tiempos de respuesta y mejorando la eficiencia del equipo de soporte.

### 1.1. Propósito

El propósito principal de este sistema es centralizar la gestión de incidencias, ofreciendo una plataforma única donde los usuarios pueden reportar problemas técnicos y el personal de OTI puede administrar y resolver dichas solicitudes de manera organizada. La aplicación también genera datos valiosos para el análisis y la toma de decisiones a través de su dashboard y módulo de reportes.

### 1.2. Alcance

El sistema abarca las siguientes funcionalidades clave:

- **Gestión de Incidencias:** Creación, asignación, actualización de estado y seguimiento de incidencias.
- **Gestión de Usuarios:** Administración de roles y permisos para Super Administradores, Administradores y Practicantes.
- **Dashboard Analítico:** Visualización de métricas y estadísticas en tiempo real.
- **Generación de Reportes:** Exportación de datos en formatos PDF y Excel.
- **Autenticación y Seguridad:** Sistema de login seguro con control de acceso basado en roles.

### 1.3. Stack Tecnológico

El proyecto está construido sobre un stack tecnológico moderno y robusto, que incluye:

- **Backend:** Python con el framework Flask.
- **Base de Datos:** SQLite, con capacidad de migración a PostgreSQL o MySQL.
- **Frontend:** HTML, CSS, y JavaScript, utilizando TailwindCSS y DaisyUI para la interfaz de usuario.
- **Librerías Adicionales:** SQLAlchemy para el ORM, Flask-Login para la autenticación, y ReportLab/OpenPyXL para la generación de reportes.

## 2. Arquitectura del Backend

El backend está desarrollado con Flask y sigue una estructura modular basada en Blueprints, lo que facilita la organización del código y la separación de responsabilidades.

### 2.1. Modelos de la Base de Datos

La base de datos se gestiona a través de SQLAlchemy y se compone de los siguientes modelos:

- **Usuario:** Almacena la información de los usuarios del sistema, incluyendo sus credenciales, roles y datos personales.
- **Incidente:** Contiene todos los detalles de las incidencias reportadas, como la descripción, prioridad, estado y personal asignado.
- **Practicante:** Guarda la información de los practicantes, incluyendo su especialidad y contacto.
- **HistorialEdicion:** Registra cada cambio realizado en una incidencia, proporcionando un historial completo de modificaciones.

### 2.2. Rutas (Blueprints)

Las rutas de la aplicación están organizadas en los siguientes Blueprints:

- **auth:** Gestiona la autenticación de usuarios (login, logout).
- **dashboard:** Proporciona los datos para el dashboard analítico.
- **incidentes:** Maneja el CRUD (Crear, Leer, Actualizar, Eliminar) de las incidencias.
- **reportes:** Genera los reportes en formato PDF y Excel.
- **practicantes:** Administra la información de los practicantes.
- **usuarios:** Permite la gestión de usuarios del sistema.
- **superadmin:** Ofrece funcionalidades exclusivas para el Super Administrador.

## 3. Arquitectura del Frontend

El frontend está construido con HTML, CSS y JavaScript, y utiliza el motor de plantillas Jinja2 de Flask. La interfaz de usuario se ha diseñado con TailwindCSS y DaisyUI, lo que proporciona un diseño moderno y responsivo.

### 3.1. Plantillas (Templates)

Las plantillas se encuentran en el directorio `app/templates` y están organizadas por funcionalidad. El archivo `base.html` sirve como plantilla principal, y las demás plantillas heredan de esta para mantener una estructura consistente.

### 3.2. Activos Estáticos (Static Assets)

Los activos estáticos, como las hojas de estilo CSS, los scripts de JavaScript y las imágenes, se encuentran en el directorio `app/static`. Estos archivos se sirven directamente al cliente y son responsables de la apariencia y el comportamiento interactivo de la aplicación.

## 4. Funcionalidades Clave

### 4.1. Gestión de Usuarios

El sistema cuenta con un sistema de roles y permisos que define el acceso de cada usuario a las diferentes funcionalidades:

- **Super Administrador:** Tiene control total sobre el sistema, incluyendo la gestión de otros administradores.
- **Administrador:** Puede gestionar incidencias y usuarios con el rol de practicante.
- **Practicante:** Puede registrar y resolver incidencias.

### 4.2. Gestión de Incidencias

El módulo de incidencias permite:

- **Crear:** Registrar nuevas incidencias con información detallada.
- **Asignar:** Asignar incidencias a uno o varios practicantes.
- **Actualizar:** Modificar el estado, la prioridad y otros detalles de una incidencia.
- **Historial:** Ver el historial de cambios de una incidencia.

### 4.3. Dashboard Analítico

El dashboard ofrece una vista general del estado de las incidencias a través de gráficos y estadísticas, permitiendo un seguimiento en tiempo real.

### 4.4. Generación de Reportes

El sistema puede generar reportes en PDF y Excel, con la posibilidad de filtrar los datos por diferentes criterios, como fechas, prioridad o tipo de incidencia.

## 5. Configuración y Despliegue

### 5.1. Configuración del Entorno de Desarrollo

Para configurar el entorno de desarrollo, sigue estos pasos:

1. **Clona el repositorio:** `git clone <URL_DEL_REPOSITORIO>`
2. **Crea un entorno virtual:** `python -m venv venv`
3. **Activa el entorno virtual:**
   - En Windows: `venv\Scripts\activate`
   - En macOS/Linux: `source venv/bin/activate`
4. **Instala las dependencias:** `pip install -r requirements.txt`
5. **Ejecuta la aplicación:** `python run.py`

### 5.2. Despliegue a Producción

Para el despliegue a producción, se recomienda utilizar un servidor de aplicaciones WSGI como Gunicorn o uWSGI, y un servidor web como Nginx para servir como proxy inverso.
