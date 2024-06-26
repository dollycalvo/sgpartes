import calendar
from datetime import datetime
from partes.views_helpers.common import CAMPO_HISTORIAL_ESTADO, CAMPO_HISTORIAL_REVISION, STATUS_PLANILLA_APROBADO, STATUS_PLANILLA_BORRADOR, STATUS_PLANILLA_PRESENTADO, TIPO_CAMBIO_MODIFICACION, enviarEmailPlanilla, nombresMeses, redirectToError, registroHistorialYEnviarMail
from partes.helper import etiquetaCodigo
from partes.models import Adjuntos, CampoHistorial, RegistroHistorial, StatusPlanilla, Planilla, RegistroDiario, TipoCambio
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage

from sgpartes import settings


def aprobarPlanilla(request):
    del request.session['idPorAprobar']
    planilla = Planilla.objects.filter(id = int(request.POST['id_planilla']))
    if len(planilla) != 1:
        return redirectToError(request, "Ha ocurrido un error al obtener la planilla de la base de datos")
    planilla = planilla[0]
    statusAprobado = StatusPlanilla.objects.filter(status = "Aprobado")[0]
    planilla.status = statusAprobado
    planilla.save()
    registroHistorialYEnviarMail(
        request,
        planilla,
        TipoCambio.objects.get(nombre = TIPO_CAMBIO_MODIFICACION),
        CampoHistorial.objects.get(nombre = CAMPO_HISTORIAL_ESTADO),
        "",
        STATUS_PLANILLA_PRESENTADO,
        STATUS_PLANILLA_APROBADO,
        False
    )
    # Enviamos el email
    enviarEmailPlanilla(planilla.id, [planilla.empleado.jefe_directo.email], True)
    request.session['dashboard_mensaje'] = "La planilla ha sido aprobada"
    return HttpResponseRedirect("/dashboard")


def revisarPlanilla(request):
    del request.session['idPorAprobar']
    planilla = Planilla.objects.filter(id = int(request.POST['id_planilla']))
    if len(planilla) != 1:
        return redirectToError(request, "Ha ocurrido un error al obtener la planilla de la base de datos")
    planilla = planilla[0]
    # Volvemos la planilla a status Borrador para que la revise el agente
    statusBorrador = StatusPlanilla.objects.filter(status = "Borrador")[0]
    planilla.status = statusBorrador
    observaciones = request.POST["observaciones"].strip()
    if observaciones == "":
        observaciones = "Por favor contacte a su jefe directo para conocer las razones de la revisión."
    planilla.observaciones = observaciones
    planilla.save()
    registroHistorialYEnviarMail(
        request,
        planilla,
        TipoCambio.objects.get(nombre = TIPO_CAMBIO_MODIFICACION),
        CampoHistorial.objects.get(nombre = CAMPO_HISTORIAL_REVISION),
        "",
        "",
        observaciones,
        False
    )
    registroHistorialYEnviarMail(
        request,
        planilla,
        TipoCambio.objects.get(nombre = TIPO_CAMBIO_MODIFICACION),
        CampoHistorial.objects.get(nombre = CAMPO_HISTORIAL_ESTADO),
        "",
        STATUS_PLANILLA_PRESENTADO,
        STATUS_PLANILLA_BORRADOR,
        False
    )
    # Enviar mail de confirmación de aprobación
    empleado = planilla.empleado
    nombre_completo_empleado = empleado.apellidos + ", " + empleado.nombres
    mensaje_email = "Fecha: " + nombresMeses[int(planilla.mes) - 1]["Nombre"] + " " + str(planilla.anio)
    mensaje_email += "\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(empleado.legajo) + ")"
    mensaje_email += "\nObservaciones: " + observaciones
    print("Mail al agente indicando que se envía a revisión la planilla")
    if settings.ENVIAR_EMAIL:
        if settings.DEBUG:
            email = EmailMessage("Planilla devuelta para revisión: " + nombre_completo_empleado, # asunto
                                    mensaje_email, # cuerpo del email
                                    "webmaster@cguimaraenz.com", # from
                                    ["webmaster@cguimaraenz.com"] # to
                                    )
        else:
            email = EmailMessage("Planilla devuelta para revisión: " + nombre_completo_empleado, # asunto
                                    mensaje_email, # cuerpo del email
                                    "mdcalvogrycn@gmail.com", # from
                                    [empleado.email] # to
                                    )
        email.send()
    request.session['dashboard_mensaje'] = "La planilla ha sido devuelta para revisión"
    return HttpResponseRedirect("/dashboard")



def mostrarPlanillaAprobacion(request):
    id_planilla = int(request.POST["id_planilla"])
    # verificamos que el ID esté dentro de la lista, como mecanismo de seguridad
    if id_planilla in request.session['idsPlanillasParaMostrar']:
        #del request.session['idsPlanillasParaMostrar']   # ya eliminamos esta lista, luego se regenerará de ser necesario
        planillas = Planilla.objects.filter(id = id_planilla)
        if len(planillas) != 1:
            mensaje_error = "No se ha encontrado la planilla"
            return render(request, "error.html", {"mensaje": mensaje_error})
        # Si tenemos la planilla:
        planilla = planillas[0]
        # Historial
        historial = RegistroHistorial.objects.filter(planilla = planilla).order_by('-fechaHora')
        # Adjuntos
        adjuntos = Adjuntos.objects.filter(planilla = planilla)
        # Verificamos que el status sea sólo PRESENTADO
        if planilla.status.status == STATUS_PLANILLA_BORRADOR:
            mensaje_error = "La planilla aún no se ha presentado."
            return render(request, "error.html", {"mensaje": mensaje_error})
        # Continuamos tomando los registros diarios
        SIN_NOVEDAD = "Sin novedad"
        dias_del_mes = range(1, calendar.monthrange(planilla.anio, planilla.mes)[1] + 1)
        datosDiarios = []
        for dia in dias_del_mes:
            datosDiarios.append(RegistroDiario(dia=dia, codigo="sn", observaciones=SIN_NOVEDAD))
        registrosDiarios = RegistroDiario.objects.filter(planilla_id=planilla.id)
        for registro in registrosDiarios:
            datosDiarios[registro.dia - 1] = registro
        # datosDiarios = RegistroDiario.objects.filter(planilla_id = planilla.id)
        if len(datosDiarios) == 0:
            mensaje_error = "No se han encontrado datos diarios de la planilla"
            return render(request, "error.html", {"mensaje": mensaje_error})
        # Ya tenemos los registros diarios, procedemos a crear el objeto de datos para el template
        request.session["idPorAprobar"] = planilla.id
        nombreMes = nombresMeses[int(planilla.mes - 1)]["Nombre"]
        request.session['id_planilla'] = planilla.id
        return render(request, "planilla_aprobacion.html", {"nombreMes": nombreMes,
                                                            "planilla": planilla,
                                                            "adjuntos": adjuntos,
                                                            "datosDiarios": datosDiarios,
                                                            "datosEmpleado": planilla.empleado,
                                                            "historial": historial,
                                                            "primerDiaDelMes": datetime.strptime("1/" + str(planilla.mes) + "/" + str(planilla.anio), "%d/%m/%Y").weekday()})

