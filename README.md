# Proyecto Django

## Requisitos

Antes de comenzar, asegurate de tener instalado:

* Python 3.12 o superior
* Git
* pip

---

## Instalación

### 1. Clonar el repositorio

Cloná el proyecto desde GitHub:

```bash
git clone https://github.com/Villada-PG3/trabajo-practico-integrador-veterinaria_-el-sabueso-feliz.git
```

Entrá a la carpeta del proyecto:

```bash
cd trabajo-practico-integrador-veterinaria_-el-sabueso-feliz
```

---

### 2. Crear el entorno virtual

Creá un entorno virtual llamado `venv`:

```bash
python -m venv venv
```

---

### 3. Activar el entorno virtual

#### Windows

En CMD:

```bash
venv\Scripts\activate
```

En PowerShell:

```bash
venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source venv/bin/activate
```

Una vez activado, deberías ver algo parecido a:

```text
(venv) C:\proyecto>
```

---

### 4. Instalar las dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

---

## 5. Aplicar las migraciones

Ejecutá:

```bash
python manage.py migrate
```

---

## 6. Crear un superusuario

Si necesitás acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Completá los campos

---

## 7. Ejecutar el proyecto

Iniciá el servidor:

```bash
python manage.py runserver
```

Si todo está correcto, vas a ver:

```text
Starting development server at http://127.0.0.1:8000/
```

Abrí en el navegador:

**http://127.0.0.1:8000/**

Para acceder al panel de administración:

**http://127.0.0.1:8000/admin/**

---

## Estructura básica

## 📁 Estructura del proyecto

```
trabajo-practico-integrador-veterinaria_-el-sabueso-feliz/
│
├── .venv/                    # Entorno virtual de Python
│
├── config/                   # Configuración principal del proyecto Django
│   ├── __pycache__/          # Archivos temporales generados por Python
│   ├── __init__.py           # Indica que config es un paquete de Python
│   ├── asgi.py               # Configuración para servidores ASGI
│   ├── settings.py           # Configuración general de Django
│   ├── urls.py               # URLs principales del proyecto
│   └── wsgi.py               # Configuración para servidores WSGI
│
├── docs/                     # Documentación del proyecto
│   ├── diagrams/             # Diagramas utilizados en el proyecto
│   ├── er/                   # Diagrama Entidad-Relación
│   ├── uml/                  # Diagramas UML
│   └── README.md             # Documentación adicional
│
├── media/                    # Archivos multimedia subidos a la aplicación
│
├── mi_app/                   # Aplicación principal de Django
│
├── static/                   # Archivos estáticos del proyecto
│                             # CSS, JavaScript, imágenes, etc.
│
├── templates/                # Plantillas HTML utilizadas por Django
│
├── .gitignore                # Archivos y carpetas ignorados por Git
│
├── db.sqlite3                # Base de datos SQLite del proyecto
│
├── manage.py                 # Herramienta de administración de Django
│
├── README.md                 # Documentación principal del proyecto
│
└── requirements.txt          # Dependencias necesarias para ejecutar el proyecto

## Importante
El `venv` se crea nuevamente en cada computadora y las dependencias se instalan mediante:

```bash
pip install -r requirements.txt
```

---

## Desarrollo

Cada vez que trabajes en el proyecto, activá primero el entorno virtual:

```bash
venv\Scripts\activate
```

y después ejecutá:

```bash
python manage.py runserver
```

Para instalar una nueva dependencia:

```bash
pip install nombre_paquete
```

Y luego actualizá `requirements.txt`:

```bash
pip freeze > requirements.txt
```