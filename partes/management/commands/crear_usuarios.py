from django.core.management.base import BaseCommand, CommandError
from partes.models import Agentes, RegistroDiario, Planilla
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # RegistroDiario.objects.all().delete()
        # Planilla.objects.all().delete()
        # return

        # pl = Planilla.objects.all()
        # for p in pl:
        #     print(str(p.id) + " " + str(p.mes) + " " + str(p.anio) + " " + str(p.agente_id) + " " + str(p.presentado))
        # print()
        # regs = RegistroDiario.objects.all()
        # for reg in regs:
        #     if reg.codigo != "sn":
        #         print(str(reg.planilla_id) + " " + str(reg.dia) + " " + reg.codigo + " " + reg.observaciones)
        # return

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
                    email_jefe_directo = "carlosguimaraenz@yahoo.com.ar",
                    password = make_password("xyx456")),
            Agentes(legajo = 77777,
                    apellidos = "Olmos",
                    nombres = "Andrea",
                    email_agente = "andrea@gmail.com",
                    jefe_directo = "Pablo López",
                    email_jefe_directo = "calito83@gmail.com",
                    password = make_password("123ggg"))
        ]
        agentesDB = Agentes.objects.all()
        for nuevoAgente in nuevosAgentes:
            i = 0
            while i < len(agentesDB) and nuevoAgente.legajo != agentesDB[i].legajo:
                i += 1
            if i >= len(agentesDB):
                nuevoAgente.save()
            else:
                agentesDB[i].apellidos = nuevoAgente.apellidos
                agentesDB[i].nombres = nuevoAgente.nombres
                agentesDB[i].email_agente = nuevoAgente.email_agente
                agentesDB[i].jefe_directo = nuevoAgente.jefe_directo
                agentesDB[i].email_jefe_directo = nuevoAgente.email_jefe_directo
                agentesDB[i].save()
        # Verificamos
        agentesDB = Agentes.objects.all()
        for agenteDB in agentesDB:
            print(str(agenteDB.id) + ": " + str(agenteDB.legajo) + " " + agenteDB.apellidos + " " + agenteDB.email_jefe_directo)
        
