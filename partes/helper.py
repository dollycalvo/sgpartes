import os
import unicodedata
import re
from django.core.files.storage import default_storage

from partes.models import PermisoEspecial
import settings
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
    carpeta = os.path.join(settings.BASE_DIR, 'sgpartes/adjuntos/')
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
    if value == "cs":
        return "CS"
    if value == "v":
        return "LAR"
    if value == "sa":
        return "SA"
    if value == "+":
        return "+"
    if value == "d":
        return "D"
    if value == "e":
        return "E"
    if value == "h":
        return "H"
    if value == "L":
        return "L"
    if value == "h":
        return "M"
    if value == "n":
        return "N"
    if value == "p":
        return "P"
    if value == "r":
        return "R"
    if value == "W":
        return "W"
    if value == "y":
        return "Y"
    if value == "z":
        return "Z"
    if value == "fr":
        return "FR"
    if value == "ja":
        return "JA"
    if value == "jh":
        return "JH"
    if value == "zd":
        return "ZD"
    if value == "cmp":
        return "CMP"
    if value == "cmt":
        return "CMT"
    if value == "cse":
        return "CSE"
    if value == "ff1":
        return "FF1"
    if value == "ff2":
        return "FF2"
    if value == "jlm":
        return "JLM"
    if value == "mex":
        return "MEX"
    if value == "qti":
        return "QTI"
    if value == "qco":
        return "QCO"
    if value == "qre":
        return "QRE"
    if value == "vre":
        return "VRE"
    if value == "x":
        return "X"
    if value == "unp":
        return "UNP"
    if value == "unt":
        return "UNT"
    if value == "unu":
        return "UNU"

    #return value.upper()
    return value


def tienePermisoEspecialRPA(id_empleado):
    rolesRPA = PermisoEspecial.objects.filter(empleado_id = id_empleado, codigo="RPA")
    if (len(rolesRPA) == 1):
        return True
    return False


def tienePermisosEspecialesParaDashboard(id_empleado):
    # De momento sólo retornará con este permiso especial, en caso de nuevos permisos especiales
    # podríamos hacer un OR para verificar si tiene alguno que le habilite acceso al dashboard
    return tienePermisoEspecialRPA(id_empleado)