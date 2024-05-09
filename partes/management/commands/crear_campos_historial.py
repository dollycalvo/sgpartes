from django.core.management.base import BaseCommand
from partes.models import CampoHistorial, TipoCambio
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Agrega los nombres de los campos y los tipos de cambio de historial'

    def handle(self, *args, **options):
        camposExistentes = CampoHistorial.objects.all()
        nuevosCampos = ["Código", "Observaciones", "Archivo adjunto", "Estado", "Observaciones para revisión"]
        if len(camposExistentes) == 0:  # Creamos los nuevos
            for nuevoCampo in nuevosCampos:
                campo = CampoHistorial(nombre = nuevoCampo)
                campo.save()
        else:   # actualizamos
            i = 0
            for campoExistente in camposExistentes:
                campoExistente.nombre = nuevosCampos[i]
                i += 1
                campoExistente.save()
            

        tiposExistentes = TipoCambio.objects.all()
        nuevosTiposCambio = ["Inserción", "Eliminación", "Modificación"]
        if len(tiposExistentes) == 0: # Creamos nuevos tipos
            for nuevoTipo in nuevosTiposCambio:
                tipo = TipoCambio(nombre = nuevoTipo)
                tipo.save()
        else: # actualizamos los existentes
            i = 0
            for tipoExistente in tiposExistentes:
                tipoExistente.nombre = nuevosTiposCambio[i]
                i += 1
                tipoExistente.save()
            
            