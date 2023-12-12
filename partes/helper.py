from django.core.files.storage import default_storage
import calendar, time

def guardarArchivo(archivo):
    new_filename = "tmp/" + archivo.name + "." + str(calendar.timegm(time.gmtime()))
    default_storage.save(new_filename, archivo)
    return new_filename