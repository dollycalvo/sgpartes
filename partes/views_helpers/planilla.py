from partes.views_helpers.common import nombresMeses, redirectToError
import calendar
from partes.helper import guardarArchivo, etiquetaCodigo
from partes.models import Empleado, StatusPlanilla, Planilla, RegistroDiario
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
    if (len(planillas) == 1):
        planilla = planillas[0]
        planilla.status = statusPlanilla
        if statusPlanilla.status == "Presentado":
            planilla.observaciones = ""
    else:
        planilla = Planilla(empleado_id = id_empleado,
                            mes = mes,
                            anio = anio,
                            status = statusPlanilla)
    # Tenemos archivo adjunto?
    datosEmpleado = Empleado.objects.filter(id = id_empleado)
    if "pdf" in request.FILES:
        nombre_archivo = ""
        try:
            nombre_archivo = guardarArchivo(request.FILES["pdf"], mes, anio, str(datosEmpleado[0].legajo) + "_" + datosEmpleado[0].apellidos)
        except:
            return redirectToError(request, "Ha ocurrido un error al intentar guardar el archivo")
        if nombre_archivo != "":
            planilla.pdf_adjunto = nombre_archivo
        else:
            return redirectToError(request, "Ha ocurrido un error al intentar guardar el archivo")
    # Guardamos los cambios en la existente o la nueva según corresponda
    planilla.save()
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
            if observacion.strip() != SIN_NOVEDAD and observacion.strip() != "":
                registro = RegistroDiario(planilla_id = planilla.id,
                                        dia = i, # día
                                        codigo = listaCodigos[i - 1],
                                        observaciones = observacion)
                registro.save()
                nuevosRegistros.append(registro)
            else:
                nuevosRegistros.append(RegistroDiario(dia = i, codigo = "sn", observaciones = ""))    # En caso de no existir ni ser creado, hacemos un dummy 
        i += 1
    # Enviamos e-mail
    if statusPlanilla.status == "Presentado":
        empleado = datosEmpleado[0]
        nombre_completo_empleado = empleado.apellidos + ", " + empleado.nombres
        mensaje_email = "Fecha: " + nombresMeses[int(mes) - 1]["Nombre"] + " " + anio
        mensaje_email += "\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(empleado.legajo) + ")"
        mensaje_email += observaciones_para_email
        print("Mail a " + empleado.jefe_directo.email)
        # Archivo adjunto
        nombre_archivo = planilla.pdf_adjunto
        carpeta = "adjuntos/"
        fl_path = carpeta + nombre_archivo
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
                        "nombreArchivoAdjunto": planilla.pdf_adjunto}
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
                        "nombreArchivoAdjunto": datosPlanilla.pdf_adjunto}
    request.session['id_planilla'] = datosPlanilla.id
    return render(request, 'planilla.html', templateParams)
