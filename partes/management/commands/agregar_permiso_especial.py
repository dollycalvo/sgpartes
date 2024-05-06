from django.core.management.base import BaseCommand
from partes.models import Empleado, PermisoEspecial
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Agrega o actualiza usuarios al sistema'

    def handle(self, *args, **options):
        existePermisoEspecial = PermisoEspecial.objects.filter(empleado_id = 62, codigo = "EFL")
        # si aún no está agregada, la agregamos
        if len(existePermisoEspecial) == 0:
            permisoEspecial = PermisoEspecial(empleado_id = 62,
                                              codigo = "EFL",
                                              descripcion = "Esta persona es la encargada de establecer una fecha límite de presentación de planilla",
                                              nombre = "Establecimiento de fecha límite")
            permisoEspecial.save()
