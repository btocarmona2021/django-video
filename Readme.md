# 📚 Apuntes Django + Docker — Videos 1 al 6

---

## 🎬 VIDEO 1 — Instalación y configuración con Docker

### Estructura del proyecto
```
proyecto/
├── docker-compose.yml
├── src/
│   └── django/          ← código fuente (mapeado al contenedor)
└── config/
    └── django_image/
        ├── Dockerfile
        └── requirements.txt
```

### requirements.txt
```
django
psycopg2
djangorestframework
djangorestframework-simplejwt
```

### Dockerfile
```dockerfile
FROM python:3.12

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gcc

WORKDIR /usr/src/app

RUN pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
services:
  backend:
    image: video-backend:0.1
    build:
      context: ./config/django_image
    volumes:
      - ./src/django:/usr/src/app:delegated
    ports:
      - "8000:8000"
    networks:
      - red

networks:
  red:
```

### Comandos de la primera vez
```bash
docker compose up                          # construye imagen (falla, es normal)
docker compose run backend bash            # entrá al contenedor
django-admin startproject app .            # creá el proyecto Django
exit
docker compose up                          # ahora sí levanta correctamente
```

### ⚠️ Concepto clave
El volumen (src/django/) se monta DESPUÉS de construir la imagen.
Por eso NO se puede poner django-admin startproject en el Dockerfile.
Se hace manualmente una sola vez desde dentro del contenedor.

### Comandos Docker útiles
```bash
docker compose up          # levantar
docker compose up -d       # levantar en background
docker compose down        # bajar y eliminar contenedores
docker compose logs backend  # ver logs
docker ps                  # ver contenedores corriendo
docker compose run backend bash   # entrar al contenedor (no está corriendo)
docker compose exec backend bash  # entrar al contenedor (ya está corriendo)
docker compose up --build  # rebuild de la imagen
```

### Solución error de permisos (Linux)
```bash
sudo chown -R $USER:$USER src/   # arregla archivos ya creados
```

---

## 🎬 VIDEO 2 — Estructura del proyecto Django

### Archivos creados por startproject
```
src/django/
├── manage.py              ← centro de control del proyecto
├── db.sqlite3             ← base de datos por defecto (temporal)
└── app/
    ├── __init__.py
    ├── settings.py        ← configuración global
    ├── urls.py            ← rutas URL raíz
    ├── asgi.py            ← producción (no tocar)
    └── wsgi.py            ← producción (no tocar)
```

### Archivos importantes en settings.py
- SECRET_KEY → clave de encriptación (cambiar en producción)
- DEBUG = True → mostrar errores detallados (False en producción)
- INSTALLED_APPS → lista de apps activas del proyecto
- MIDDLEWARE → capas de procesamiento de cada petición
- DATABASES → configuración de base de datos

### Crear la app aulas
```bash
docker compose exec backend bash   # entrar al contenedor
python manage.py startapp aulas    # crear la app
exit
```
⚠️ Siempre crear apps desde DENTRO del contenedor

### Registrar la app en settings.py
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",   # ← agregar
    "aulas",            # ← agregar
]
```

### Cambio de idioma/zona horaria (recomendado)
```python
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
```

### Estructura de la app aulas
```
aulas/
├── __init__.py     ← indica que es un paquete Python
├── admin.py        ← registra modelos en el panel de administración
├── apps.py         ← configuración específica de esta app
├── models.py       ← define las tablas de la base de datos ⭐
├── views.py        ← funciones que responden a peticiones HTTP ⭐
├── tests.py        ← tests automatizados
└── migrations/     ← cambios de base de datos (generados automáticamente)
```

### Comandos manage.py más usados
```bash
python manage.py runserver          # levantar servidor de desarrollo
python manage.py startapp nombre    # crear nueva aplicación
python manage.py makemigrations     # detectar cambios en modelos
python manage.py migrate            # aplicar cambios a la base de datos
python manage.py shell              # consola interactiva Python+Django
python manage.py help               # ver todos los comandos disponibles
```

---

## 🎬 VIDEO 3 — Git + Primera View + URLs

### Subir proyecto a GitHub
```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### .gitignore recomendado
```
.idea/
.vscode/
*.pyc
```

### Primera vista en aulas/views.py
```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hola mundo")
```

### Crear aulas/urls.py (no existe por defecto, hay que crearlo)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
]
```

### Conectar en app/urls.py (raíz)
```python
from django.contrib import admin
from django.urls import path, include   # ← importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aulas/', include('aulas.urls')),
]
```

### ⚠️ Concepto clave — Flujo de una petición
URL → app/urls.py → aulas/urls.py → views.py → respuesta al cliente
La URL y el nombre de la función NO tienen que coincidir, son independientes.

---

## 🎬 VIDEO 4 — Parámetros en URLs

### views.py actualizado
```python
from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hola mundo")

def bye(request):
    return HttpResponse("Hasta luego")

def edad(request, anos, futuro):
    current_year = datetime.date.today().year
    incremento = futuro - current_year
    cumplira = anos + incremento
    mensaje = "En el año %d cumplirás %d años" % (futuro, cumplira)
    return HttpResponse(mensaje)
```

### aulas/urls.py actualizado
```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('bye/', views.bye),
    path('edad/<int:anos>/<int:futuro>/', views.edad),
]
```

### URLs de prueba
- http://localhost:8000/aulas/hello/
- http://localhost:8000/aulas/bye/
- http://localhost:8000/aulas/edad/30/2030/

### ⚠️ Concepto clave — Parámetros en URL
Sintaxis: <tipo:nombre_variable>
Tipos disponibles: int, str, slug, uuid, path
Los parámetros de la URL se reciben como argumentos en la función de views.py

---

## 🎬 VIDEO 5 — Templates (Parte 1)

### Estructura de carpetas
```
aulas/
└── templates/
    ├── primer_plantilla.html
    ├── segunda_plantilla.html
    └── tercer_plantilla.html
```

### Verificar APP_DIRS en settings.py
```python
TEMPLATES = [
    {
        ...
        'APP_DIRS': True,   # ← busca en aulas/templates/ automáticamente
        ...
    },
]
```

### Las 3 formas de usar templates (de peor a mejor)

#### Forma 1 — MAL (template en variable string)
```python
from django.http import HttpResponse
from django.template import Template, Context

def primer_plantilla(request):
    plantilla = "<h1>Hola {{ nombre }}</h1>"
    tpl = Template(plantilla)
    ctx = Context({"nombre": "Juan Pérez"})
    return HttpResponse(tpl.render(ctx))
```

#### Forma 2 — MEJOR (template en archivo)
```python
from django.template.loader import get_template

def segunda_plantilla(request):
    tpl = get_template("segunda_plantilla.html")
    mensaje = tpl.render({"nombre": "Juan Pérez"})
    return HttpResponse(mensaje)
```

#### Forma 3 — CORRECTA ✅ (shortcut render)
```python
from django.shortcuts import render
import datetime

def tercer_plantilla(request):
    return render(request, "tercer_plantilla.html", {
        "nombre": "Pedro González",
        "fecha_actual": datetime.date.today()
    })
```

### HTML de las plantillas
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Hola, {{ nombre }}</h1>
    <p>Hoy es: {{ fecha_actual|date:"Y-m-d" }}</p>
</body>
</html>
```

### aulas/urls.py con las nuevas URLs
```python
urlpatterns = [
    path('hello/', views.hello),
    path('bye/', views.bye),
    path('edad/<int:anos>/<int:futuro>/', views.edad),
    path('plantilla1/', views.primer_plantilla),
    path('plantilla2/', views.segunda_plantilla),
    path('plantilla3/', views.tercer_plantilla),
]
```

### ⚠️ Concepto clave
Siempre usar render() — hace todo en una línea:
get_template + Context + HttpResponse = render(request, "template.html", {})

---

## 🎬 VIDEO 6 — Templates (Parte 2) — Objetos, for e if

### Agregar clase y vista en views.py
```python
class Empleado(object):
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

def cuarta_plantilla(request):
    empleado = Empleado("Juan", "Gómez")
    laborables = ["lunes", "martes", "miércoles", "jueves", "viernes"]
    return render(request, "cuarta_plantilla.html", {
        "mi_empleado": empleado,
        "fecha_actual": datetime.date.today(),
        "dias_laborables": laborables,
    })
```

### cuarta_plantilla.html
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Cuarta plantilla</h1>

    <p>Nombre: <strong>{{ mi_empleado.nombre }}</strong>
               <em>{{ mi_empleado.apellido }}</em></p>

    <p>Año: {{ fecha_actual.year }}</p>
    <p>Mes: {{ fecha_actual.month }}</p>
    <p>Día: {{ fecha_actual.day }}</p>

    <p>Días laborables:</p>
    {% if dias_laborables %}
    <ul>
        {% for elemento in dias_laborables %}
        <li>{{ elemento }}</li>
        {% endfor %}
    </ul>
    {% endif %}

</body>
</html>
```

### Agregar URL en aulas/urls.py
```python
path('plantilla4/', views.cuarta_plantilla),
```

### Sintaxis del sistema de templates Django
| Sintaxis | Uso |
|---|---|
| {{ variable }} | Imprimir variable |
| {{ objeto.propiedad }} | Acceder a propiedad de objeto |
| {{ fecha|date:"Y-m-d" }} | Aplicar filtro a variable |
| {% for x in lista %}...{% endfor %} | Recorrer lista |
| {% if condicion %}...{% endif %} | Bloque condicional |

### ⚠️ Concepto clave
Pasar objetos completos al contexto en lugar de strings armados en Python.
Esto le da libertad al diseñador para manejar la presentación en el HTML
sin tocar el código Python.

---

## 📋 Estado actual del proyecto

### views.py completo (aulas/views.py)
```python
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
import datetime

def hello(request):
    return HttpResponse("Hola mundo")

def bye(request):
    return HttpResponse("Hasta luego")

def edad(request, anos, futuro):
    current_year = datetime.date.today().year
    incremento = futuro - current_year
    cumplira = anos + incremento
    mensaje = "En el año %d cumplirás %d años" % (futuro, cumplira)
    return HttpResponse(mensaje)

def primer_plantilla(request):
    plantilla = "<h1>Hola {{ nombre }}</h1>"
    tpl = Template(plantilla)
    ctx = Context({"nombre": "Juan Pérez"})
    return HttpResponse(tpl.render(ctx))

def segunda_plantilla(request):
    tpl = get_template("segunda_plantilla.html")
    fecha_actual = datetime.date.today()
    mensaje = tpl.render({"nombre": "Juan Pérez", "fecha_actual": fecha_actual})
    return HttpResponse(mensaje)

def tercer_plantilla(request):
    return render(request, "tercer_plantilla.html", {
        "nombre": "Pedro González",
        "fecha_actual": datetime.date.today()
    })

class Empleado(object):
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

def cuarta_plantilla(request):
    empleado = Empleado("Juan", "Gómez")
    laborables = ["lunes", "martes", "miércoles", "jueves", "viernes"]
    return render(request, "cuarta_plantilla.html", {
        "mi_empleado": empleado,
        "fecha_actual": datetime.date.today(),
        "dias_laborables": laborables,
    })
```

### urls.py completo (aulas/urls.py)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('bye/', views.bye),
    path('edad/<int:anos>/<int:futuro>/', views.edad),
    path('plantilla1/', views.primer_plantilla),
    path('plantilla2/', views.segunda_plantilla),
    path('plantilla3/', views.tercer_plantilla),
    path('plantilla4/', views.cuarta_plantilla),
]
```

### URLs disponibles para probar
- http://localhost:8000/aulas/hello/
- http://localhost:8000/aulas/bye/
- http://localhost:8000/aulas/edad/30/2030/
- http://localhost:8000/aulas/plantilla1/
- http://localhost:8000/aulas/plantilla2/
- http://localhost:8000/aulas/plantilla3/
- http://localhost:8000/aulas/plantilla4/