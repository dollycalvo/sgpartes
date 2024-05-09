import os
import calendar
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from partes.helper import etiquetaCodigo

from partes.models import Adjuntos, Planilla, RegistroDiario
import settings

MSG_EXITO = "exito"

DIA_LIMITE_PRESENTACION_PLANILLA = 25

nombresMeses = [{"ID": 1, "Nombre": "Enero"},
                {"ID": 2, "Nombre": "Febrero"},
                {"ID": 3, "Nombre": "Marzo"},
                {"ID": 4, "Nombre": "Abril"},
                {"ID": 5, "Nombre": "Mayo"},
                {"ID": 6, "Nombre": "Junio"},
                {"ID": 7, "Nombre": "Julio"},
                {"ID": 8, "Nombre": "Agosto"},
                {"ID": 9, "Nombre": "Septiembre"},
                {"ID": 10, "Nombre": "Octubre"},
                {"ID": 11, "Nombre": "Noviembre"},
                {"ID": 12, "Nombre": "Diciembre"}]


def obtenerNombreMes(numeroMes):
    return nombresMeses[numeroMes - 1]["Nombre"]


def redirectToError(request, mensaje):
    request.session["mensaje_error"] = mensaje
    return HttpResponseRedirect("/error")


# Esta función devuelve las planillas para revisar para el empleado dado
def obtenerPlanillasParaRevisar(id_empleado):
    planillas = Planilla.objects.filter(empleado_id = id_empleado, status_id = 1).exclude(observaciones = "").order_by("anio", "mes")
    listaPlanillas = []
    for planilla in planillas:
        listaPlanillas.append({"id": planilla.id, "mes": obtenerNombreMes(planilla.mes), "anio": planilla.anio, "observaciones": planilla.observaciones})
    return listaPlanillas


def enviarEmailPlanilla(id_planilla, receptores_email, enviar_adjunto = True):
    planilla = Planilla.objects.filter(id = id_planilla)
    if len(planilla) != 1:
        return False
    try:
        planilla = planilla[0]
        # Enviar mail
        empleado = planilla.empleado
        nombre_completo_empleado = empleado.apellidos + ", " + empleado.nombres
        mensaje_email = "Fecha: " + nombresMeses[int(planilla.mes) - 1]["Nombre"] + " " + str(planilla.anio)
        mensaje_email += "\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(empleado.legajo) + ")"

        # Con el ID de la planilla, ahora creamos un registro para cada día
        registrosCoincidentes = RegistroDiario.objects.filter(planilla_id = planilla.id).order_by("dia")
        dias_del_mes = range(1, calendar.monthrange(int(planilla.anio), int(planilla.mes))[1] + 1)
        observaciones = []
        for i in dias_del_mes:
            observaciones.append("\nDía " + str(i) + ": S/N: Sin novedad")
        for registroDiario in registrosCoincidentes:
            observaciones[registroDiario.dia - 1] = "\nDía " + str(registroDiario.dia) + ": " + etiquetaCodigo(registroDiario.codigo) + ": " + registroDiario.observaciones
        observaciones_para_email = "\n" + "".join(observaciones)
        mensaje_email += observaciones_para_email

        if settings.ENVIAR_EMAIL:
            if settings.DEBUG:
                email = EmailMessage("Planilla aprobada: " + nombre_completo_empleado, # asunto
                                        mensaje_email, # cuerpo del email
                                        "webmaster@cguimaraenz.com", # from
                                        ["webmaster@cguimaraenz.com"] # to
                                        )
            else:
                email = EmailMessage("Planilla aprobada: " + nombre_completo_empleado, # asunto
                                        mensaje_email, # cuerpo del email
                                        "mdcalvogrycn@gmail.com", # from
                                        receptores_email # to
                                        )
            if enviar_adjunto == True:
                carpeta = os.path.join(settings.BASE_DIR, 'sgpartes/adjuntos/')
                adjuntos = Adjuntos.objects.filter(planilla = planilla)
                for adjunto in adjuntos:
                    nombre_archivo = adjunto.nombre_archivo
                    fl_path = carpeta + nombre_archivo
                    email.attach_file(fl_path)
            email.send()
    except:
        return False
    
    
def excedeDiaLimite(diaLimite, mes, anio):
    hoy = datetime.now()
    fechaLimite = datetime(int(anio), int(mes), diaLimite) + timedelta(days=1)
    return (hoy > fechaLimite)