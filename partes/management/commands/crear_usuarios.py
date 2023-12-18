from django.core.management.base import BaseCommand, CommandError
from partes.models import Empleado, Puesto, StatusPlanilla, RegistroDiario, Planilla
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Agrega o actualiza usuarios al sistema'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # RegistroDiario.objects.all().delete()
        # Planilla.objects.all().delete()
        # return

        # pl = Planilla.objects.all()
        # for p in pl:
        #     print(str(p.id) + " " + str(p.mes) + " " + str(p.anio) + " " + str(p.empleado_id) + " " + str(p.presentado))
        # print()
        # regs = RegistroDiario.objects.all()
        # for reg in regs:
        #     if reg.codigo != "sn":
        #         print(str(reg.planilla_id) + " " + str(reg.dia) + " " + reg.codigo + " " + reg.observaciones)
        # return
        
        nuevosStatus = [
            StatusPlanilla(status = "Borrador"),
            StatusPlanilla(status = "Presentado"),
            StatusPlanilla(status = "Aprobado")
        ]

        statusesDB = StatusPlanilla.objects.all()
        for nuevoStatus in nuevosStatus:
            i = 0
            while i < len(statusesDB) and nuevoStatus.status != statusesDB[i].status:
                i += 1
            if i >= len(statusesDB):
                nuevoStatus.save()
            else:
                statusesDB[i].status = nuevoStatus.status
                statusesDB[i].save()
        # Verificamos
        statusesDB = StatusPlanilla.objects.all()
        for statusDB in statusesDB:
            print(str(statusDB.id) + ": " + statusDB.status)

        
        nuevosPuestos = [
            Puesto(nombre = "Agente"),
            Puesto(nombre = "Supervisor"),
            Puesto(nombre = "Gerente")
        ]

        puestosDB = Puesto.objects.all()
        for nuevoPuesto in nuevosPuestos:
            i = 0
            while i < len(puestosDB) and nuevoPuesto.nombre != puestosDB[i].nombre:
                i += 1
            if i >= len(puestosDB):
                nuevoPuesto.save()
            else:
                puestosDB[i].nombre = nuevoPuesto.nombre
                puestosDB[i].save()
        # Verificamos
        puestosDB = Puesto.objects.all()
        for puestoDB in puestosDB:
            print(str(puestoDB.id) + ": " + puestoDB.nombre)

        return
        jefe = Empleado(legajo = 999555,
                    apellidos = "Jefezón",
                    nombres = "Juan Pablo",
                    email = "jpjefezon@gmail.com",
                    puesto = puestosDB[1],
                    password = make_password("abc123"))
        jefe.save()

        nuevosEmpleados = [
            Empleado(legajo = 12345,
                    apellidos = "Calvo",
                    nombres = "María Dolores",
                    email = "mdcalvo@gmail.com",
                    puesto = puestosDB[0],
                    jefe_directo = jefe,
                    password = make_password("abc123")),
            Empleado(legajo = 67890,
                    apellidos = "Guimaraenz",
                    nombres = "Carlos Roberto",
                    email = "calito83@gmail.com",
                    puesto = puestosDB[0],
                    jefe_directo = jefe,
                    password = make_password("xyx456")),
            Empleado(legajo = 77777,
                    apellidos = "Olmos",
                    nombres = "Andrea",
                    email = "andrea@gmail.com",
                    puesto = puestosDB[0],
                    jefe_directo = jefe,
                    password = make_password("123ggg"))
        ]
        empleadosDB = Empleado.objects.all()
        for nuevoEmpleado in nuevosEmpleados:
            i = 1
            while i < len(empleadosDB) and nuevoEmpleado.legajo != empleadosDB[i].legajo:
                i += 1
            if i >= len(empleadosDB):
                nuevoEmpleado.save()
            else:
                empleadosDB[i].apellidos = nuevoEmpleado.apellidos
                empleadosDB[i].nombres = nuevoEmpleado.nombres
                empleadosDB[i].email = nuevoEmpleado.email
                empleadosDB[i].puesto = nuevoEmpleado.puesto
                empleadosDB[i].jefe_directo = jefe
                empleadosDB[i].save()
        # Verificamos
        empleadosDB = Empleado.objects.all()
        for empleadoDB in empleadosDB:
            jefe_mail = empleadoDB.jefe_directo.email if empleadoDB.jefe_directo is not None else "sin jefe"
            print(str(empleadoDB.id) + ": " + str(empleadoDB.legajo) + " " + empleadoDB.apellidos + " " + jefe_mail)
        
