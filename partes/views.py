import datetime
import calendar
from partes.models import Agentes, Planilla, RegistroDiario
from partes.forms import FormSeleccionFecha
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.shortcuts import render

# Create your views here.
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

def inicio(request):
    # return HttpResponse("<h1>Bienvenido al sistema SGPARTES</h1>")
    return render(request, 'index.html');



def planilla(request):
    # Cláusula de guarda
    if 'usuario' not in request.session:
        request.session['mensaje_unauth'] = "Se requiere iniciar sesión para acceder a esta sección"
        return HttpResponseRedirect("/error")

    SIN_NOVEDAD = "Sin novedad"
    acciones_submit = ['guardar', 'presentar', 'sin_accion']
    id_agente = request.session['id_agente']
    datosAgente = Agentes.objects.filter(id=id_agente)
    # Si recibimos desde la planilla el POST
    if request.method == "POST":
        mes = request.POST['mesReporte']
        anio = request.POST['anioReporte']
        dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
        presentado = request.POST['accion_submit'] == acciones_submit[1]
        # Ya existe una planilla para este mes y agente?
        planillas = Planilla.objects.filter(agente_id=id_agente, anio=anio, mes=mes)
        if (len(planillas) == 1):
            planilla = planillas[0]
            planilla.presentado = presentado
        else:
            planilla = Planilla(agente_id = id_agente,
                                mes = mes,
                                anio = anio,
                                presentado = presentado)
        # Guardamos los cambios en la existente o la nueva según corresponda
        planilla.save()
        print("ID de planilla: " + str(planilla.id))
        # Obtengo todos los registros existentes para esa planilla, para evitar consultar por cada registro individualmente
        registrosCoincidentes = RegistroDiario.objects.filter(planilla_id = planilla.id)
        # Con el ID de la planilla, ahora creamos un registro para cada día
        nuevosRegistros = []
        i = 1
        listaCodigos = request.POST.getlist("codigos")
        for observacion in request.POST.getlist("observaciones"):
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
                if observacion.strip() != SIN_NOVEDAD:
                    registro = RegistroDiario(planilla_id = planilla.id,
                                            dia = i, # día
                                            codigo = listaCodigos[i - 1],
                                            observaciones = observacion)
                    registro.save()
                    nuevosRegistros.append(registro)
                else:
                    nuevosRegistros.append(None)    # En caso de no existir ni ser creado, hacemos un dummy 
            i += 1
        templateParams = {  "accion_submit": acciones_submit[2],
                            "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                            "datosAgente": datosAgente[0],
                            "datosPlanilla": planilla,
                            "datosDiarios": nuevosRegistros,
                            "mesReporte": int(mes),
                            "nombreMesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                            "anioReporte": anio,
                            "diasDelMes": dias_del_mes,
                            "presentado": presentado,
                            "mostrarMensaje": True,
                            "textoSinNovedad": SIN_NOVEDAD}
        
        return render(request, 'planilla.html', templateParams)
    else:   # Sino, al ser GET viene redireccionado desde la selección de fecha
        accion_submit = acciones_submit[0]
        if not 'mesReporte' in request.session:
            return HttpResponseRedirect("/error")
        mes = request.session['mesReporte']
        anio = request.session['anioReporte']
        del request.session['mesReporte']
        del request.session['anioReporte']
        dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
    datosPlanilla = Planilla.objects.filter(agente_id=id_agente, mes=mes, anio=anio)
    if len(datosPlanilla) == 1:
        datosPlanilla = datosPlanilla[0]
        datosDiarios = RegistroDiario.objects.filter(planilla_id=datosPlanilla.id)
        if len(datosDiarios) == 0:
            datosDiarios = [None] * len(dias_del_mes)
    else:
        # datosPlanilla = [0, id_agente, mes, anio, False]
        datosPlanilla = Planilla(agente_id = id_agente,
                            mes = mes,
                            anio = anio,
                            presentado = False)
        datosDiarios = [None] * len(dias_del_mes)
    templateParams = {  "accion_submit": accion_submit,
                        "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                        "datosAgente": datosAgente[0],
                        "datosPlanilla": datosPlanilla,
                        "datosDiarios": datosDiarios,
                        "mesReporte": int(mes),
                        "nombreMesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                        "anioReporte": anio,
                        "diasDelMes": dias_del_mes,
                        "textoSinNovedad": SIN_NOVEDAD}
    return render(request, 'planilla.html', templateParams)



def seleccionfecha(request):
    # Cláusula de guarda
    if 'usuario' not in request.session:
        request.session['mensaje_unauth'] = "Se requiere iniciar sesión para acceder a esta sección"
        return HttpResponseRedirect("/error")
    
    if request.method == 'POST':
        form = FormSeleccionFecha(request.POST)
        if form.is_valid():
            request.session['mesReporte'] = request.POST['mesReporte']
            request.session['anioReporte'] = request.POST['anioReporte']
            return HttpResponseRedirect('/planilla')
    else:
        form = FormSeleccionFecha()
    fechaActual = datetime.datetime.now()
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    anios = list(range(anioActual - 3, anioActual + 2))
    return render(request, 'seleccionfecha.html', {"form": form, 
                                                   "anios": anios, 
                                                   "nombresMeses": nombresMeses, 
                                                   "mesActual": mesActual, 
                                                   "anioActual": anioActual})



def login(request):
    MAX_LOGINS_INCORRECTOS = 3
    if (request.method == "GET"):
        mensaje = ""
        if 'logout' in request.GET:
            del request.session['usuario']
            del request.session['nombre_usuario']
            del request.session['logins_incorrectos']
            mensaje = "La sesión se ha cerrado correctamente"
        if 'logins_incorrectos' not in request.session:
            request.session['logins_incorrectos'] = MAX_LOGINS_INCORRECTOS
        return render(request, 'login.html', {"mensaje": mensaje})
    else: #method POST, deberíamos tener datos de usuario
        usuario = request.POST['login_username'].strip()
        password = request.POST['login_password']
        if usuario.find("@") != -1:
            agentes = Agentes.objects.filter(email_agente = usuario)
        elif usuario.isnumeric():
            agentes = Agentes.objects.filter(legajo = usuario)
        else:
            request.session['logins_incorrectos'] -= 1
            if request.session['logins_incorrectos'] == 0:
                return HttpResponseRedirect("/error?cod=1")
            mensaje_error = f"Los datos de inicio de sesión son incorrectos. Restan {request.session['logins_incorrectos']} intentos."
            return render(request, 'login.html', {"mensaje_error": mensaje_error, "usuario_previo": usuario})
        if len(agentes) == 1:   # encontramos al usuario?
            if check_password(password, agentes[0].password):
                request.session['id_agente'] = agentes[0].id
                request.session['usuario'] = agentes[0].legajo
                request.session['nombre_usuario'] = agentes[0].apellidos + ", " + agentes[0].nombres
                return HttpResponseRedirect("/seleccionfecha")
            else:   # volvemos a pedir login y aumentamos la cantidad de logins incorrectos
                request.session['logins_incorrectos'] -= 1
                if request.session['logins_incorrectos'] == 0:
                    return HttpResponseRedirect("/error?cod=1")
                mensaje_error = f"Los datos de inicio de sesión son incorrectos. Restan {request.session['logins_incorrectos']} intentos."
                return render(request, 'login.html', {"mensaje_error": mensaje_error, "usuario_previo": usuario})
        else:
            request.session['logins_incorrectos'] -= 1
            if request.session['logins_incorrectos'] == 0:
                return HttpResponseRedirect("/error?cod=1")
            mensaje_error = f"Los datos de inicio de sesión son incorrectos. Restan {request.session['logins_incorrectos']} intentos."
            return render(request, 'login.html', {"mensaje_error": mensaje_error, "usuario_previo": usuario})
    

def error(request):
    mensaje = "Se ha producido un error"
    if request.method == 'GET':
        if 'mensaje_unauth' in request.session:
            mensaje = request.session['mensaje_unauth']
            del request.session['mensaje_unauth']
        if 'logins_incorrectos' in request.session:
            del request.session['logins_incorrectos']
        if 'cod' in request.GET:
            if request.GET['cod'] == "1":
                mensaje = "Demasiados intentos incorrectos de inicio de sesión"
    return render(request, 'error.html', {"mensaje": mensaje})
