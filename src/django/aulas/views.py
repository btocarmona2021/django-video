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


# Forma 1 - MAL (template en variable string, solo para entender el concepto)
def primer_plantilla(request):
    plantilla = """
    <!DOCTYPE html><html><body>
    <h1>Hola, {{ nombre }}</h1>
    </body></html>
    """
    tpl = Template(plantilla)
    ctx = Context({"nombre": "Juan Pérez"})
    mensaje = tpl.render(ctx)
    return HttpResponse(mensaje)


# Forma 2 - MEJOR (template en archivo externo)
def segunda_plantilla(request):
    tpl = get_template("segunda_plantilla.html")
    fecha_actual = datetime.date.today()
    mensaje = tpl.render({"nombre": "Juan Pérez", "fecha_actual": fecha_actual})
    return HttpResponse(mensaje)


# Forma 3 - LA CORRECTA (shortcut render)
def tercer_plantilla(request):
    fecha_actual = datetime.date.today()
    return render(
        request,
        "tercer_plantilla.html",
        {"nombre": "Pedro González", "fecha_actual": fecha_actual},
    )


class Empleado(object):
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido


def cuarta_plantilla(request):
    empleado = Empleado("Juan", "Gómez")
    laborables = ["lunes", "martes", "miércoles", "jueves", "viernes"]
    return render(
        request,
        "cuarta_plantilla.html",
        {
            "mi_empleado": empleado,
            "fecha_actual": datetime.date.today(),
            "dias_laborables": laborables,
        },
    )
