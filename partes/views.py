import hashlib
import calendar
from datetime import datetime
from partes.models import Empleado, Puesto, StatusPlanilla, Planilla, RegistroDiario, RegeneracionPW
from partes.forms import FormSeleccionFecha
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.core.mail import send_mail

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
        # Guardamos los cambios en la existente o la nueva según corresponda
        planilla.save()
        print("ID de planilla: " + str(planilla.id))
        # Obtengo todos los registros existentes para esa planilla, para evitar consultar por cada registro individualmente
        registrosCoincidentes = RegistroDiario.objects.filter(planilla_id = planilla.id)
        # Con el ID de la planilla, ahora creamos un registro para cada día
        observaciones_para_email = "\n"
        nuevosRegistros = []
        i = 1
        listaCodigos = request.POST.getlist("codigos")
        for observacion in request.POST.getlist("observaciones"):
            observaciones_para_email += "\nDía " + str(i) + ": " + listaCodigos[i - 1] + ": " + (observacion.strip() if observacion.strip() != "" else SIN_NOVEDAD) 
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
        # Enviamos e-mail
        if statusPlanilla.status == "Presentado":
            empleado = datosEmpleado[0]
            nombre_completo_empleado = empleado.apellidos + ", " + empleado.nombres
            mensaje_email = "Fecha: " + nombresMeses[int(mes) - 1]["Nombre"] + " " + anio
            mensaje_email += "\nEmpleado: " + nombre_completo_empleado + " (legajo: " + str(empleado.legajo) + ")"
            mensaje_email += observaciones_para_email
            print("Mail a " + empleado.jefe_directo.email)
            send_mail(
                "Planilla presentada: " + nombre_completo_empleado,
                mensaje_email,
                # empleado.email,
                # [empleado.jefe_directo.email, empleado.email],
                'webmaster@cguimaraenz.com',
                ['webmaster@cguimaraenz.com'],
                fail_silently=False,
            )
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
    datosPlanilla = Planilla.objects.filter(empleado_id=id_empleado, mes=mes, anio=anio)
    if len(datosPlanilla) == 1:
        datosPlanilla = datosPlanilla[0]
        datosDiarios = RegistroDiario.objects.filter(planilla_id=datosPlanilla.id)
        if len(datosDiarios) == 0:
            datosDiarios = [None] * len(dias_del_mes)
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
        else:
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
    fechaActual = datetime.now()
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    anios = list(range(anioActual - 3, anioActual + 2))
    return render(request, 'dashboard.html', {"form": form, 
                                                   "anios": anios, 
                                                   "nombresMeses": nombresMeses, 
                                                   "mesActual": mesActual, 
                                                   "anioActual": anioActual,
                                                   "dashboard_habilitado": True})
