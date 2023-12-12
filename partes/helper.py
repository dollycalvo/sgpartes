import unicodedata
import re
from django.core.files.storage import default_storage
#import calendar, time

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


def guardarArchivo(archivo, mes, anio, empleado):
    carpeta = "adjuntos/"
    partes_nombre = archivo.name.split(".")
    # nuevo_nombre = []
    # for parte in partes_nombre:
    #     nuevo_nombre.append(slugify(parte))
    # new_filename = str(calendar.timegm(time.gmtime())) + "." + ".".join(nuevo_nombre)
    new_filename = slugify(empleado) + "_" + mes + "_" + anio + "." + partes_nombre[len(partes_nombre) - 1]
    default_storage.save(carpeta + new_filename, archivo)
    return new_filename

def etiquetaCodigo(value):
    # Convierte el código en una etiqueta para el usuario
    if value == "sn":
        return "S/N"
    if value == "cs":
        return "CS"
    if value == "v":
        return "V"
    if value == "sa":
        return "SA"
    return value