import os
import calendar
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from partes.helper import etiquetaCodigo

from partes.models import Adjuntos, Empleado, Planilla, RegistroDiario, RegistroHistorial
from sgpartes import settings

TIPO_CAMBIO_INSERCION = "Inserción"
TIPO_CAMBIO_ELIMINACION = "Eliminación"
TIPO_CAMBIO_MODIFICACION = "Modificación"

CAMPO_HISTORIAL_CODIGO = "Código"
CAMPO_HISTORIAL_OBSERVACIONES = "Observaciones"
CAMPO_HISTORIAL_ARCHIVO_ADJUNTO = "Archivo adjunto"
CAMPO_HISTORIAL_ESTADO = "Estado"
CAMPO_HISTORIAL_REVISION = "Observaciones para revisión"

STATUS_PLANILLA_BORRADOR = "Borrador"
STATUS_PLANILLA_PRESENTADO = "Presentado"
STATUS_PLANILLA_APROBADO = "Aprobado"

ACLARACION_VACIO = "(vacío)"

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


def registroHistorialYEnviarMail(request, planilla, tipo, campo, diaCambio, anterior, nuevo, enviarMail = True):
    try:
        fechaHora = datetime.now()
        nuevoRegistroHistorial = RegistroHistorial(
                            planilla = planilla,
                            fechaHora = fechaHora,
                            tipo = tipo,
                            campo = campo,
                            diaCambio = diaCambio,
                            anterior = anterior,
                            nuevo = nuevo
        )
        nuevoRegistroHistorial.save()
        # Enviamos el email
        if enviarMail and settings.ENVIAR_EMAIL:
            nombre_completo_empleado = planilla.empleado.apellidos + ", " + planilla.empleado.nombres
            if diaCambio != "":
                campo = campo.nombre + ", día " + diaCambio
            else:
                campo = campo.nombre
            cuerpo_email = "Cambios en la planilla:"
            cuerpo_email += "\n\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(planilla.empleado.legajo) + ")"
            cuerpo_email += "\nFecha y hora del cambio: " + str(fechaHora)
            cuerpo_email += "\nFecha de la planilla: " + nombresMeses[planilla.mes - 1]["Nombre"] + " " + str(planilla.anio)
            cuerpo_email += "\nTipo de cambio: " + tipo.nombre
            cuerpo_email += "\nCampo: " + campo
            cuerpo_email += "\nValor anterior: \"" + anterior + "\""
            cuerpo_email += "\nNuevo valor: \"" + nuevo + "\""
            if settings.DEBUG:
                email = EmailMessage("Cambios en la planilla: " + nombre_completo_empleado, # asunto
                                    cuerpo_email, # cuerpo del email
                                    # empleado.email,
                                    # [empleado.jefe_directo.email, empleado.email],
                                    "webmaster@cguimaraenz.com", # from
                                    ["webmaster@cguimaraenz.com"] # to
                                    )
            else:
                secretaria = Empleado.objects.filter(legajo = 20343).get()
                email = EmailMessage("Cambios en la planilla: " + nombre_completo_empleado, # asunto
                                    cuerpo_email, # cuerpo del email
                                    planilla.empleado.email, #from
                                    [secretaria.email], #to
                                    )
            # # Archivos adjuntos
            # carpeta = os.path.join(settings.BASE_DIR, 'sgpartes/adjuntos/')
            # for adjunto in adjuntos:
            #     nombre_archivo = adjunto.nombre_archivo
            #     fl_path = carpeta + nombre_archivo
            #     email.attach_file(fl_path)
            email.send()
    except Exception as e:
        print("ERROR: " + repr(e))
        return redirectToError(request, "Ha ocurrido un error al intentar guardar el historial y enviar el e-mail. Error GHEM001")
    
   
# Identificamos si una planilla está en revisión al estar en BORRADOR y tener OBSERVACIONES 
def isPlanillaEnRevision(planilla):
    return planilla.status.status == STATUS_PLANILLA_BORRADOR and planilla.observaciones.strip() != ""