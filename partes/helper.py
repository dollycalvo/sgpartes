import unicodedata
import re
from django.core.files.storage import default_storage

from partes.models import PermisoEspecial
#import calendar, time

diasDeLaSemana = [
    {"nombre": "Lunes", "corto": "Lun"},
    {"nombre": "Martes", "corto": "Mar"},
    {"nombre": "Miércoles", "corto": "Mié"},
    {"nombre": "Jueves", "corto": "Jue"},
    {"nombre": "Viernes", "corto": "Vie"},
    {"nombre": "Sábado", "corto": "Sáb"},
    {"nombre": "Domingo", "corto": "Dom"}
]

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def guardarArchivo(archivo, mes, anio, empleado, indice):
    carpeta = "adjuntos/"
    partes_nombre = archivo.name.split(".")
    # nuevo_nombre = []
    # for parte in partes_nombre:
    #     nuevo_nombre.append(slugify(parte))
    # new_filename = str(calendar.timegm(time.gmtime())) + "." + ".".join(nuevo_nombre)
    new_filename = slugify(empleado) + "_" + mes + "_" + anio + "_" + str(indice) + "." + partes_nombre[len(partes_nombre) - 1]
    default_storage.save(carpeta + new_filename, archivo)
    return new_filename

def etiquetaCodigo(value):
    # Convierte el código en una etiqueta para el usuario
    if value == "sn":
        return "S/N"

    return value.upper()


def tienePermisoEspecialRPA(id_empleado):
    rolesRPA = PermisoEspecial.objects.filter(empleado_id = id_empleado, codigo="RPA")
    if (len(rolesRPA) == 1):
        return True
    return False


def tienePermisosEspecialesParaDashboard(id_empleado):
    # De momento sólo retornará con este permiso especial, en caso de nuevos permisos especiales
    # podríamos hacer un OR para verificar si tiene alguno que le habilite acceso al dashboard
    return tienePermisoEspecialRPA(id_empleado)