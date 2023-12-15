from django.core.files.storage import default_storage
from django.http import HttpResponse
import mimetypes
import hashlib
import calendar
from partes.helper import guardarArchivo, etiquetaCodigo
from datetime import datetime
from partes.models import Empleado, StatusPlanilla, Planilla, RegistroDiario, RegeneracionPW
from partes.forms import FormSeleccionFecha
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.core.mail import EmailMessage, send_mail


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
    return login(request)


def planilla(request):    
    # Cláusula de guarda
    if 'usuario' not in request.session:
        request.session['mensaje_unauth'] = "Se requiere iniciar sesión para acceder a esta sección"
        return HttpResponseRedirect("/error")

    SIN_NOVEDAD = "Sin novedad"
    acciones_submit = ['guardar', 'presentar', 'sin_accion']
    id_empleado = request.session['id_empleado']
    datosEmpleado = Empleado.objects.filter(id=id_empleado)
    # Si recibimos desde la planilla el POST
    if request.method == "POST":
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
        else:
            planilla = Planilla(empleado_id = id_empleado,
                                mes = mes,
                                anio = anio,
                                status = statusPlanilla)
        # Tenemos archivo adjunto?
        if "pdf" in request.FILES:
            nombre_archivo = ""
            try:
                nombre_archivo = guardarArchivo(request.FILES["pdf"], mes, anio, str(datosEmpleado[0].legajo) + "_" + datosEmpleado[0].apellidos)
            except:
                request.session['mensaje_error'] = "Ha ocurrido un error al intentar guardar el archivo"
                return HttpResponseRedirect("/error")            
            if nombre_archivo != "":
                planilla.pdf_adjunto = nombre_archivo
            else:
                request.session['mensaje_error'] = "Ha ocurrido un error al intentar guardar el archivo"
                return HttpResponseRedirect("/error")            
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
                    nuevosRegistros.append(RegistroDiario(dia = i, codigo = "sn", observaciones = SIN_NOVEDAD))    # En caso de no existir ni ser creado, hacemos un dummy 
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
            email = EmailMessage("Planilla presentada: " + nombre_completo_empleado, # asunto
                                 mensaje_email, # cuerpo del email
                                # empleado.email,
                                # [empleado.jefe_directo.email, empleado.email],
                                "webmaster@cguimaraenz.com", # from
                                ["webmaster@cguimaraenz.com"] # to
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
        return render(request, 'planilla.html', templateParams)
    else:   # Sino, al ser GET viene redireccionado desde la selección de fecha
        accion_submit = acciones_submit[0]
        if not 'mesReporte' in request.session:
            return HttpResponseRedirect("/seleccionfecha")
        mes = request.session['mesReporte']
        anio = request.session['anioReporte']
        del request.session['mesReporte']
        del request.session['anioReporte']
    dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
    datosPlanilla = Planilla.objects.filter(empleado_id=id_empleado, mes=mes, anio=anio)
    if len(datosPlanilla) == 1:
        datosDiarios = []
        for dia in dias_del_mes:
            datosDiarios.append(RegistroDiario(dia=dia, codigo="sn", observaciones=SIN_NOVEDAD))
        datosPlanilla = datosPlanilla[0]
        registrosDiarios = RegistroDiario.objects.filter(planilla_id=datosPlanilla.id)
        for registro in registrosDiarios:
            datosDiarios[registro.dia - 1] = registro
    else:
        # datosPlanilla = [0, id_empleado, mes, anio, False]
        datosPlanilla = Planilla(empleado_id = id_empleado,
                            mes = mes,
                            anio = anio,
                            status = StatusPlanilla.objects.filter(status = "Borrador")[0])
        datosDiarios = [None] * len(dias_del_mes)
    templateParams = {  "accion_submit": accion_submit,
                        "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                        "datosEmpleado": datosEmpleado[0],
                        "datosPlanilla": datosPlanilla,
                        "datosDiarios": datosDiarios,
                        "mesReporte": int(mes),
                        "nombreMesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                        "anioReporte": anio,
                        "diasDelMes": dias_del_mes,
                        "textoSinNovedad": SIN_NOVEDAD,
                        "nombreArchivoAdjunto": datosPlanilla.pdf_adjunto}
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
    fechaActual = datetime.now()
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
            if 'usuario' in request.session:
                del request.session['usuario']
            if 'nombre_usuario' in request.session:
                del request.session['nombre_usuario']
            if 'logins_incorrectos' in request.session:
                del request.session['logins_incorrectos']
            if 'dashboard_habilitado' in request.session:
                del request.session['dashboard_habilitado']
            if 'id_empleado' in request.session:
                del request.session['id_empleado']
            if 'id_planilla' in request.session:
                del request.session['id_planilla']
            if 'puesto' in request.session:
                del request.session['puesto']
            mensaje = "La sesión se ha cerrado correctamente"
        else:
            # Si no estoy haciendo logout
            if 'usuario' in request.session:
                # Si vuelvo al link /login y ya estoy logueado, voy a seleccion de fecha o dashboard según corresponda
                if request.session['puesto'] == "Agente":
                    return HttpResponseRedirect("/seleccionfecha")
                else:
                    # Si es supervisor o gerente, va a una página de selección de acción
                    return HttpResponseRedirect("/dashboard")
        if 'logins_incorrectos' not in request.session:
            request.session['logins_incorrectos'] = MAX_LOGINS_INCORRECTOS
        return render(request, 'login.html', {"mensaje": mensaje})
    else: #method POST, deberíamos tener datos de usuario
        usuario = request.POST['login_username'].strip()
        password = request.POST['login_password']
        if usuario.find("@") != -1:
            empleados = Empleado.objects.filter(email = usuario)
        elif usuario.isnumeric():
            empleados = Empleado.objects.filter(legajo = usuario)
        else:
            if 'logins_incorrectos' in request.session:
                request.session['logins_incorrectos'] -= 1
            else:
                request.session['logins_incorrectos'] = MAX_LOGINS_INCORRECTOS
            if request.session['logins_incorrectos'] == 0:
                return HttpResponseRedirect("/error?cod=1")
            mensaje_error = f"Los datos de inicio de sesión son incorrectos. Restan {request.session['logins_incorrectos']} intentos."
            return render(request, 'login.html', {"mensaje_error": mensaje_error, "usuario_previo": usuario})
        if len(empleados) == 1:   # encontramos al usuario?
            if check_password(password, empleados[0].password):
                request.session['id_empleado'] = empleados[0].id
                request.session['usuario'] = empleados[0].legajo
                request.session['nombre_usuario'] = empleados[0].apellidos + ", " + empleados[0].nombres
                request.session['puesto'] = empleados[0].puesto.nombre
                if empleados[0].puesto.nombre == "Agente":
                    return HttpResponseRedirect("/seleccionfecha")
                else:
                    # Si es supervisor o gerente, va a una página de selección de acción
                    request.session['dashboard_habilitado'] = True
                    return HttpResponseRedirect("/dashboard")
            else:   # volvemos a pedir login y aumentamos la cantidad de logins incorrectos
                if 'logins_incorrectos' in request.session:
                    request.session['logins_incorrectos'] -= 1
                else:
                    request.session['logins_incorrectos'] = MAX_LOGINS_INCORRECTOS
                if request.session['logins_incorrectos'] == 0:
                    return HttpResponseRedirect("/error?cod=1")
                mensaje_error = f"Los datos de inicio de sesión son incorrectos. Restan {request.session['logins_incorrectos']} intentos."
                return render(request, 'login.html', {"mensaje_error": mensaje_error, "usuario_previo": usuario})
        else: # Si no encontramos al usuario
            if 'logins_incorrectos' in request.session:
                request.session['logins_incorrectos'] -= 1
            else:
                request.session['logins_incorrectos'] = MAX_LOGINS_INCORRECTOS
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
        if 'mensaje_error' in request.session:
            mensaje = request.session['mensaje_error']
            del request.session['mensaje_error']
        if 'logins_incorrectos' in request.session:
            del request.session['logins_incorrectos']
        if 'cod' in request.GET:
            if request.GET['cod'] == "1":
                mensaje = "Demasiados intentos incorrectos de inicio de sesión"
    return render(request, 'error.html', {"mensaje": mensaje})



def regenerar(request):
    MAX_ERRORES = 2
    acciones = ["pedir_email", "form_regenerar", "crear_pw"]
    if request.method == 'POST':
        # En el POST hay dos posibilidades:
        if "accion" in request.POST:
            # Tomamos el email y generamos el código para enviarle el link
            if request.POST["accion"] == acciones[0]:
                usuario = request.POST['username'].strip()
                if usuario.find("@") != -1:
                    empleados = Empleado.objects.filter(email = usuario)
                elif usuario.isnumeric():
                    empleados = Empleado.objects.filter(legajo = usuario)
                else:
                    mensaje_error = "La información ingresada no corresponde a ningún usuario activo"
                    return render(request, "regenerar.html", {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[0]})
                # Al llegar aquí, deberíamos tener la consulta hecha (aunque no haya coincidencias)
                if len(empleados) == 1:
                    empleado = empleados[0]
                    # Primero verificamos que no exista otro previo, o sino lo actualizamos
                    RegeneracionPW.objects.filter(empleado_id = empleado.id).delete()
                    # Creamos el link y lo enviamos por e-mail
                    str2hash = empleado.email + str(datetime.now())
                    nuevo_codigo = hashlib.sha256(str2hash.encode()).hexdigest()
                    regPW = RegeneracionPW(empleado_id = empleado.id, codigo = nuevo_codigo)
                    regPW.save()
                    # Enviamos el e-mail
                    base_url = request.build_absolute_uri('/')[:-1].strip("/")
                    cuerpo_email = "Estimado(a) " + empleado.nombres + " " + empleado.apellidos + ",\n"
                    cuerpo_email += "por favor, ingrese al siguiente link (si no funciona, copie y pegue en su navegador), "
                    cuerpo_email += "e ingrese su e-mail o legajo, nueva contraseña y confirmación.\n\n" + base_url
                    cuerpo_email += "/regenerar?codigo=" + str(regPW.codigo) + "\n\nAdministradores del Sistema"
                    send_mail(
                        "Instrucciones para regenerar su contraseña",
                        cuerpo_email,
                        # webmaster@sistema.com,
                        # [empleado.email],
                        'webmaster@cguimaraenz.com',
                        ['webmaster@cguimaraenz.com'],
                        fail_silently=False)
                    # Y redireccionamos con el mensaje de éxito
                    mensaje = "Se ha envíado un correo electrónico a su casilla con información para regenerar su contraseña"
                    return render(request, "regenerar.html", {"mensaje": mensaje})
                else:
                    mensaje_error = "La información ingresada no corresponde a ningún usuario activo"
                    return render(request, "regenerar.html", {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[0]})
            else:
                # O tomamos el mail, el nuevo password, la confirmación, y verificamos que coincida con el codigo
                codigo = request.POST["codigo"]
                pw = request.POST["password"]
                confirmar_pw = request.POST["confirmar_password"]
                if pw != confirmar_pw:
                    mensaje_error = "La contraseña y la confirmación no coinciden"
                    return render(request, 'regenerar.html', {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[1], "codigo": request.POST["codigo"]})
                usuario = request.POST['username'].strip()
                if usuario.find("@") != -1:
                    empleados = Empleado.objects.filter(email = usuario)
                elif usuario.isnumeric():
                    empleados = Empleado.objects.filter(legajo = usuario)
                if len(empleados) == 1:
                    # Si hay un usuario, seguimos con la verificación
                    empleado = empleados[0]
                    regsPW = RegeneracionPW.objects.filter(empleado_id = empleado.id)
                    if len(regsPW) == 1:
                        if regsPW[0].codigo == codigo:
                            # Regeneramos el password
                            empleado.password = make_password(pw)
                            empleado.save()
                            # Elimino el código para que no se vuelva a utilizar
                            regsPW.delete()
                            mensaje = "La contraseña se ha regenerado correctamente. Ya puede utilizarla para iniciar sesión"
                            return render(request, 'regenerar.html', {"mensaje": mensaje, "acciones": acciones, "accion": acciones[2], "codigo": request.POST["codigo"]})
                        else:
                            mensaje_error = "Hay un error en el código suministrado. Verifique que el correo electrónico desde el cual siguió el link sea el más reciente."
                            return render(request, 'regenerar.html', {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[2], "codigo": request.POST["codigo"]})
                    else:
                        mensaje_error = "No existe ningún pedido de regeneración de contraseña para este usuario!"
                        return render(request, 'regenerar.html', {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[2], "codigo": request.POST["codigo"]})
                else:
                    # Sino, mensaje de error
                    if 'errores_intentos' in request.session:
                        if request.session['errores_intentos'] > 1:
                            request.session['errores_intentos'] -= 1
                            mensaje_error = "Los datos de usuario ingresados son incorrectos. Restan " + str(request.session['errores_intentos']) + " intentos"
                            return render(request, 'regenerar.html', {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[1], "codigo": request.POST["codigo"], "errores_intentos": request.session['errores_intentos']})
                        else:
                            del request.session['errores_intentos']
                            return render(request, "error.html", {"mensaje": "Demasiados intentos incorrectos para regenerar la contraseña"})
                    else:
                        request.session['errores_intentos'] = MAX_ERRORES
                        mensaje_error = "Los datos de usuario ingresados son incorrectos. Restan " + str(request.session['errores_intentos']) + " intentos"
                        return render(request, 'regenerar.html', {"mensaje_error": mensaje_error, "acciones": acciones, "accion": acciones[1], "codigo": request.POST["codigo"], "errores_intentos": request.session['errores_intentos']})
        return render(request, "error.html")
    else: # GET method
        if 'codigo' in request.GET: # si viene desde el link enviado a su email
            return render(request, 'regenerar.html', {"acciones": acciones, "accion": acciones[1], "codigo": request.GET["codigo"]})
        else: # si viene desde el login, simplemente mostramos el formulario con el campo email
            return render(request, 'regenerar.html', {"acciones": acciones, "accion": acciones[0]})


def dashboard(request):
        # Cláusula de guarda
    if 'puesto' not in request.session or request.session['puesto'] == "Agente":
        request.session['mensaje_unauth'] = "No tienes acceso a este contenido. Si se trata de un error, contacta al administrador del sistema."
        return HttpResponseRedirect("/error")
    
    if request.method == 'POST':
        form = FormSeleccionFecha(request.POST)
        if form.is_valid():
            request.session['mesReporte'] = request.POST['mesReporte']
            request.session['anioReporte'] = request.POST['anioReporte']
            return HttpResponseRedirect('/planilla')
    else:   # GET request
        form = FormSeleccionFecha()
        # Datos de los empleados a cargo
        statusPlanillaPresentado = StatusPlanilla.objects.filter(status = "Presentado")[0]
        subordinados = Empleado.objects.filter(jefe_directo = request.session['id_empleado']).order_by("apellidos", "nombres")
        listaPlanillas = []
        soloIDsPlanillas = []
        for subordinado in subordinados:            
            planillasPorAprobar = Planilla.objects.filter(empleado = subordinado, status = statusPlanillaPresentado).order_by("anio", "mes")
            if len(planillasPorAprobar) > 0:
                planillasDeEmpleado = {"id": subordinado.id,
                                    "nombre_completo": subordinado.apellidos + ", " + subordinado.nombres,
                                    "planillasPorAprobar": []
                                    }
                for planilla in planillasPorAprobar:
                    soloIDsPlanillas.append(planilla.id)
                    planillasDeEmpleado["planillasPorAprobar"].append({"id": planilla.id, "mes": nombresMeses[int(planilla.mes) - 1], "anio": planilla.anio})
                listaPlanillas.append(planillasDeEmpleado)
        # Guardamos la lista en la sesión para verificarla posteriormente al procesarla,
        # para evitar que un supervisor acceda a una planilla a la cual no está autorizado
        request.session['idsPlanillasPorAprobar'] = soloIDsPlanillas
            
    fechaActual = datetime.now()
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    anios = list(range(anioActual - 3, anioActual + 2))
    mensaje = ""
    if "dashboard_mensaje" in request.session:
        mensaje = request.session['dashboard_mensaje']
        del request.session['dashboard_mensaje']
    return render(request, 'dashboard.html', {"form": form, 
                                                   "mensaje": mensaje,
                                                   "anios": anios, 
                                                   "nombresMeses": nombresMeses, 
                                                   "mesActual": mesActual, 
                                                   "anioActual": anioActual,
                                                   "listaPlanillas": listaPlanillas})



def aprobar(request):
    if request.method == "GET":
        request.session['mensaje_unauth'] = "Esta página sólo puede ser accedida desde el dashboard."
        return HttpResponseRedirect("/error")
    if request.method == 'POST':
        if "aprobar" in request.POST and request.POST["aprobar"] == "1":
            if not "idPorAprobar" in request.session:
                request.session['mensaje_error'] = "Ha ocurrido un error al procesar el ID de la planilla"
                return HttpResponseRedirect("/error")
            if not "id_planilla" in request.POST or request.session["idPorAprobar"] != int(request.POST["id_planilla"]):
                request.session['mensaje_error'] = "Ha ocurrido un error al procesar el ID de la planilla"
                return HttpResponseRedirect("/error")
            # Si obtenemos el ID en el request, y coincide con el existente en la sesión, seguimos
            del request.session['idPorAprobar']
            planilla = Planilla.objects.filter(id = int(request.POST['id_planilla']))
            if len(planilla) != 1:
                request.session['mensaje_error'] = "Ha ocurrido un error al obtener la planilla de la base de datos"
                return HttpResponseRedirect("/error")
            planilla = planilla[0]
            statusAprobado = StatusPlanilla.objects.filter(status = "Aprobado")[0]
            planilla.status = statusAprobado
            planilla.save()
            # Enviar mail de confirmación de aprobación
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
            print("Mail al jefe indicando que se aprobó una planilla")

            nombre_archivo = planilla.pdf_adjunto
            carpeta = "adjuntos/"
            fl_path = carpeta + nombre_archivo
            email = EmailMessage("Planilla aprobada: " + nombre_completo_empleado, # asunto
                                 mensaje_email, # cuerpo del email
                                 "webmaster@cguimaraenz.com", # from
                                 ["webmaster@cguimaraenz.com"] # to
                                 )
            email.attach_file(fl_path)
            email.send()
            request.session['dashboard_mensaje'] = "La planilla ha sido aprobada"
            return HttpResponseRedirect("/dashboard")
        if "id_planilla" in request.POST:
            id_planilla = int(request.POST["id_planilla"])
            # verificamos que el ID esté dentro de la lista, como mecanismo de seguridad
            if id_planilla in request.session['idsPlanillasPorAprobar']:
                #del request.session['idsPlanillasPorAprobar']   # ya eliminamos esta lista, luego se regenerará de ser necesario
                planillas = Planilla.objects.filter(id = id_planilla)
                if len(planillas) != 1:
                    mensaje_error = "No se ha encontrado la planilla"
                    return render(request, "error.html", {"mensaje": mensaje_error})
                # Si tenemos la planilla:
                planilla = planillas[0]
                # Verificamos que el status sea sólo PRESENTADO
                if planilla.status.status == "Borrador":
                    mensaje_error = "La planilla aún no se ha presentado."
                    return render(request, "error.html", {"mensaje": mensaje_error})
                elif planilla.status.status == "Aprobado":                
                    mensaje_error = "La planilla ya ha sido aprobada."
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
                                                                    "datosDiarios": datosDiarios,
                                                                    "datosEmpleado": planilla.empleado})
    return render(request, 'index.html')


def download_file(request):
    planillas = Planilla.objects.filter(id = request.session['id_planilla'])
    if len(planillas) != 1:
        request.session['mensaje_error'] = "No se ha encontrado la planilla"
        return HttpResponseRedirect("/error")
    nombre_archivo = planillas[0].pdf_adjunto
    carpeta = "adjuntos/"
    fl_path = carpeta + nombre_archivo
    try:
        fl = open(fl_path, "rb")
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % nombre_archivo
    except:
        request.session['mensaje_error'] = "No se ha encontrado el archivo adjunto"
        return HttpResponseRedirect("/error")
    return response