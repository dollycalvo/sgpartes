from django.core.management.base import BaseCommand
from partes.models import CampoHistorial, TipoCambio
from django.contrib.auth.hashers import make_password

from partes.views_helpers.common import CAMPO_HISTORIAL_ARCHIVO_ADJUNTO, CAMPO_HISTORIAL_CODIGO, CAMPO_HISTORIAL_ESTADO, CAMPO_HISTORIAL_OBSERVACIONES, CAMPO_HISTORIAL_REVISION, TIPO_CAMBIO_ELIMINACION, TIPO_CAMBIO_INSERCION, TIPO_CAMBIO_MODIFICACION

class Command(BaseCommand):
    help = 'Agrega los nombres de los campos y los tipos de cambio de historial'

    def handle(self, *args, **options):
        camposExistentes = CampoHistorial.objects.all()
        nuevosCampos = [CAMPO_HISTORIAL_CODIGO, CAMPO_HISTORIAL_OBSERVACIONES, CAMPO_HISTORIAL_ARCHIVO_ADJUNTO, CAMPO_HISTORIAL_ESTADO, CAMPO_HISTORIAL_REVISION]
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
        nuevosTiposCambio = [TIPO_CAMBIO_INSERCION, TIPO_CAMBIO_ELIMINACION, TIPO_CAMBIO_MODIFICACION]
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
            
            