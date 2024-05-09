import os
from datetime import datetime
from partes.views_helpers.common import nombresMeses, redirectToError
import calendar
from partes.helper import guardarArchivo, etiquetaCodigo
from partes.models import Adjuntos, Empleado, StatusPlanilla, Planilla, RegistroDiario
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage

import settings


SIN_NOVEDAD = "Sin novedad"
acciones_submit = ['guardar', 'presentar', 'sin_accion']


def procesarCambiosEnPlanilla(request, id_empleado):
    mes = request.POST['mesReporte']
    anio = request.POST['anioReporte']
    dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
    if request.POST['accion_submit'] == acciones_submit[1]:
        statusPlanilla = StatusPlanilla.objects.filter(status = "Presentado")[0]
    else:
        statusPlanilla = StatusPlanilla.objects.filter(status = "Borrador")[0]
    # Ya existe una planilla para este mes y empleado?
    planillas = Planilla.objects.filter(empleado_id=id_empleado, anio=anio, mes=mes)
    indice_adjunto = 1
    if (len(planillas) == 1):
        planilla = planillas[0]
        planilla.status = statusPlanilla
        if statusPlanilla.status == "Presentado":
            planilla.observaciones = ""
        # cantidad de adjuntos?
        indice_adjunto = len(Adjuntos.objects.filter(planilla = planilla)) + 1
    else:
        planilla = Planilla(empleado_id = id_empleado,
                            mes = mes,
                            anio = anio,
                            status = statusPlanilla)
    # Guardamos los cambios en la existente o la nueva según corresponda
    planilla.save()
    # Tenemos archivo adjunto?
    datosEmpleado = Empleado.objects.filter(id = id_empleado)
    if "pdfs" in request.FILES:
        for archivo in request.FILES.getlist("pdfs"):
            nombre_archivo = ""
            try:
                nombre_archivo = guardarArchivo(archivo, mes, anio, str(datosEmpleado[0].legajo) + "_" + datosEmpleado[0].apellidos, indice_adjunto)
                indice_adjunto += 1
            except Exception as e:
                print("ERROR: " + repr(e))
                return redirectToError(request, "Ha ocurrido un error al intentar guardar los archivos. Error GA001")
            if nombre_archivo != "":
                adjunto = Adjuntos(planilla = planilla, nombre_archivo = nombre_archivo)
                adjunto.save()
            else:
                return redirectToError(request, "Ha ocurrido un error al intentar guardar los archivos. Error GA002")
    adjuntos = Adjuntos.objects.filter(planilla = planilla)
    # Obtengo todos los registros existentes para esa planilla, para evitar consultar por cada registro individualmente
    registrosCoincidentes = RegistroDiario.objects.filter(planilla_id = planilla.id)
    # Con el ID de la planilla, ahora creamos un registro para cada día
    observaciones_para_email = "\n"
    nuevosRegistros = []
    i = 1
    listaCodigos = request.POST.getlist("codigos")
    for observacion in request.POST.getlist("observaciones"):
        observaciones_para_email += "\nDía " + str(i) + ": " + etiquetaCodigo(listaCodigos[i - 1]) + ": " + (observacion.strip() if observacion.strip() != "" else SIN_NOVEDAD)
        rcIndex = 0
        while rcIndex < len(registrosCoincidentes) and registrosCoincidentes[rcIndex].dia != i:
            rcIndex += 1
        # Si ya existe en la base de datos, lo actualizamos, contenga lo que contenga
        if rcIndex < len(registrosCoincidentes):
            registro = registrosCoincidentes[rcIndex]
            registro.codigo = listaCodigos[i - 1]
            registro.observaciones = observacion
            registro.save()
            nuevosRegistros.append(registro)
        else: # Sino, creamos uno nuevo siempre y cuando sea sin novedad
            if (listaCodigos[i - 1] != "sn"):
                registro = RegistroDiario(planilla_id = planilla.id,
                                        dia = i, # día
                                        codigo = listaCodigos[i - 1],
                                        observaciones = observacion)
                registro.save()
                nuevosRegistros.append(registro)
            else:
                # En caso de no existir ni ser creado, hacemos un dummy
                nuevosRegistros.append(RegistroDiario(dia = i, codigo = "sn", observaciones = ""))
        i += 1
    # Enviamos e-mail
    if statusPlanilla.status == "Presentado":
        empleado = datosEmpleado[0]
        nombre_completo_empleado = empleado.apellidos + ", " + empleado.nombres
        if settings.ENVIAR_EMAIL:
            mensaje_email = "Fecha: " + nombresMeses[int(mes) - 1]["Nombre"] + " " + anio
            mensaje_email += "\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(empleado.legajo) + ")"
            mensaje_email += observaciones_para_email
            print("Mail a " + empleado.jefe_directo.email)
            if settings.DEBUG:
                email = EmailMessage("Planilla presentada: " + nombre_completo_empleado, # asunto
                                        mensaje_email, # cuerpo del email
                                    # empleado.email,
                                    # [empleado.jefe_directo.email, empleado.email],
                                    "webmaster@cguimaraenz.com", # from
                                    ["webmaster@cguimaraenz.com"] # to
                                    )
            else:
                email = EmailMessage("Planilla presentada: " + nombre_completo_empleado, # asunto
                                        mensaje_email, # cuerpo del email
                                    empleado.email, #from
                                    [empleado.jefe_directo.email, empleado.email], #to
                                    )
            # Archivos adjuntos
            carpeta = os.path.join(settings.BASE_DIR, 'sgpartes/adjuntos/')
            for adjunto in adjuntos:
                nombre_archivo = adjunto.nombre_archivo
                fl_path = carpeta + nombre_archivo
                email.attach_file(fl_path)
            email.send()
    # Nos preparamos para renderizar la página
    templateParams = {  "accion_submit": acciones_submit[2],
                        "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                        "datosEmpleado": datosEmpleado[0],
                        "datosPlanilla": planilla,
                        "datosDiarios": nuevosRegistros,
                        "mesReporte": int(mes),
                        "nombreMesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                        "anioReporte": anio,
                        "diasDelMes": dias_del_mes,
                        "statusPlanilla": statusPlanilla.status,
                        "mostrarMensaje": True,
                        "textoSinNovedad": SIN_NOVEDAD,
                        "nombresArchivosAdjuntos": adjuntos,
                        "primerDiaDelMes": datetime.strptime("1/" + str(planilla.mes) + "/" + str(planilla.anio), "%d/%m/%Y").weekday()
                    }
    request.session['id_planilla'] = planilla.id
    return render(request, 'planilla.html', templateParams)


def mostrarPlanillaParaVistaEdicion(request, id_empleado = 0, id_planilla = "0"):
    accion_submit = acciones_submit[0]
    if not 'mesReporte' in request.session and id_planilla == "0":
        return HttpResponseRedirect("/seleccionfecha")
    if id_planilla == "0":
        mes = request.session['mesReporte']
        anio = request.session['anioReporte']
        del request.session['mesReporte']
        del request.session['anioReporte']
        datosPlanilla = Planilla.objects.filter(empleado_id = id_empleado, mes = mes, anio = anio)
    else:
        datosPlanilla = Planilla.objects.filter(id = id_planilla)
    if len(datosPlanilla) == 1:
        datosPlanilla = datosPlanilla[0]
        # obtenemos sus archivos adjuntos
        adjuntos = Adjuntos.objects.filter(planilla_id = datosPlanilla.id)
        datosDiarios = []
        dias_del_mes = range(1, calendar.monthrange(int(datosPlanilla.anio), int(datosPlanilla.mes))[1] + 1)
        for dia in dias_del_mes:
            datosDiarios.append(RegistroDiario(dia = dia, codigo = "sn", observaciones = ""))
        registrosDiarios = RegistroDiario.objects.filter(planilla_id=datosPlanilla.id)
        for registro in registrosDiarios:
            datosDiarios[registro.dia - 1] = registro
    else:
        # datosPlanilla = [0, id_empleado, mes, anio, False]
        dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
        datosPlanilla = Planilla(empleado_id = id_empleado,
                            mes = mes,
                            anio = anio,
                            status = StatusPlanilla.objects.filter(status = "Borrador")[0])
        datosDiarios = [None] * len(dias_del_mes)
        adjuntos = None
    datosEmpleado = Empleado.objects.filter(id = id_empleado)[0]
    templateParams = {  "accion_submit": accion_submit,
                        "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                        "datosEmpleado": datosEmpleado,
                        "datosPlanilla": datosPlanilla,
                        "datosDiarios": datosDiarios,
                        "mesReporte": int(datosPlanilla.mes),
                        "nombreMesReporte": nombresMeses[int(datosPlanilla.mes) - 1]["Nombre"],
                        "anioReporte": datosPlanilla.anio,
                        "diasDelMes": dias_del_mes,
                        "textoSinNovedad": SIN_NOVEDAD,
                        "nombresArchivosAdjuntos": adjuntos,
                        "primerDiaDelMes": datetime.strptime("1/" + str(datosPlanilla.mes) + "/" + str(datosPlanilla.anio), "%d/%m/%Y").weekday()
                    }
    request.session['id_planilla'] = datosPlanilla.id
    return render(request, 'planilla.html', templateParams)
