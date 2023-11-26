from django.core.management.base import BaseCommand, CommandError
from partes.models import Agentes
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        nuevosAgentes = [
            Agentes(legajo = 12345,
                    apellidos = "Calvo",
                    nombres = "María Dolores",
                    email_agente = "mdcalvo@gmail.com",
                    jefe_directo = "Juan Pérez",
                    email_jefe_directo = "jperez@gmail.com",
                    password = make_password("abc123")),
            Agentes(legajo = 67890,
                    apellidos = "Guimaraenz",
                    nombres = "Carlos Roberto",
                    email_agente = "calito83@gmail.com",
                    jefe_directo = "Pablo López",
                    email_jefe_directo = "plopez@gmail.com",
                    password = make_password("xyx456")),
            Agentes(legajo = 77777,
                    apellidos = "Olmos",
                    nombres = "Andrea",
                    email_agente = "andrea@gmail.com",
                    jefe_directo = "Pablo López",
                    email_jefe_directo = "plopez@gmail.com",
                    password = make_password("123ggg"))
        ]
        agentesDB = Agentes.objects.all()
        for nuevoAgente in nuevosAgentes:
            i = 0
            while i < len(agentesDB) and nuevoAgente.legajo != agentesDB[i].legajo:
                i += 1
            if i >= len(agentesDB):
                nuevoAgente.save()
        # Verificamos
        agentesDB = Agentes.objects.all()
        for agenteDB in agentesDB:
            print(str(agenteDB.id) + ": " + str(agenteDB.legajo) + " " + agenteDB.apellidos)
        
