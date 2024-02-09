from django.core.management.base import BaseCommand, CommandError
from partes.models import Agentes, RegistroDiario, Planilla, RegeneracionPW
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Muestra la información en la tabla de regeneración de contraseñas'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        regPWs = RegeneracionPW.objects.all()
        for regPW in regPWs:
            print(str(regPW.agente_id) + ": " + regPW.codigo)
