from partes.views_helpers.common import nombresMeses, redirectToError
from partes.views_helpers.regenerar import generarCodigo, crearNuevoPassword
from partes.views_helpers.dashboard import cargarPlanillasPorAprobarYCalendario
from partes.views_helpers.planilla import mostrarPlanillaParaVistaEdicion, procesarCambiosEnPlanilla
from partes.views_helpers.aprobar import aprobarPlanilla, mostrarPlanillaAprobacion
from partes.views_helpers.login import procesarLogout, buscarUsuario
from django.http import HttpResponse
import mimetypes
from datetime import datetime
from partes.models import Empleado, Planilla
from partes.forms import FormSeleccionFecha
from django.http import HttpResponseRedirect
from django.shortcuts import render


def inicio(request):
    return login(request)


def planilla(request):
    # Cláusula de guarda
    if 'usuario' not in request.session:
        return redirectToError(request, "Se requiere iniciar sesión para acceder a esta sección")
    id_empleado = request.session['id_empleado']
    datosEmpleado = Empleado.objects.filter(id=id_empleado)
    # Si recibimos desde la planilla el POST
    if request.method == "POST":
        return procesarCambiosEnPlanilla(request, id_empleado, datosEmpleado)
    else:   # Sino, al ser GET viene redireccionado desde la selección de fecha
        return mostrarPlanillaParaVistaEdicion(request, id_empleado, datosEmpleado)


def seleccionfecha(request):
    # Cláusula de guarda
    if 'usuario' not in request.session:
        return redirectToError(request, "Se requiere iniciar sesión para acceder a esta sección.")
    
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
            mensaje = procesarLogout(request)
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
        return buscarUsuario(request, MAX_LOGINS_INCORRECTOS)


def error(request):
    mensaje = "Se ha producido un error"
    if request.method == 'GET':
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
    acciones = ["pedir_email", "form_regenerar", "crear_pw"]
    if request.method == 'POST':
        # En el POST hay dos posibilidades:
        if "accion" in request.POST:
            # Tomamos el email y generamos el código para enviarle el link
            if request.POST["accion"] == acciones[0]:
                return generarCodigo(request, acciones)
            else:
                # O tomamos el mail, el nuevo password, la confirmación, y verificamos que coincida con el codigo
                return crearNuevoPassword(request, acciones)
        return render(request, "error.html")
    else: # GET method
        if 'codigo' in request.GET: # si viene desde el link enviado a su email
            return render(request, 'regenerar.html', {"acciones": acciones, "accion": acciones[1], "codigo": request.GET["codigo"]})
        else: # si viene desde el login, simplemente mostramos el formulario con el campo email
            return render(request, 'regenerar.html', {"acciones": acciones, "accion": acciones[0]})


def dashboard(request):
    # Cláusula de guarda
    if 'puesto' not in request.session or request.session['puesto'] == "Agente":
        return redirectToError(request, "No tienes acceso a este contenido. Si se trata de un error, contacta al administrador del sistema.")
    
    # Si es POST, procesamos el pedido de mirar/editar su propia planilla
    if request.method == 'POST':
        form = FormSeleccionFecha(request.POST)
        if form.is_valid():
            request.session['mesReporte'] = request.POST['mesReporte']
            request.session['anioReporte'] = request.POST['anioReporte']
            return HttpResponseRedirect('/planilla')
    else:   # GET request
        return cargarPlanillasPorAprobarYCalendario(request)


def aprobar(request):
    if request.method == "GET":
        return redirectToError(request, "Esta página sólo puede ser accedida desde el dashboard.")
    if request.method == 'POST':
        if "aprobar" in request.POST and request.POST["aprobar"] == "1":
            if not "idPorAprobar" in request.session:
                return redirectToError(request, "Ha ocurrido un error al procesar el ID de la planilla")
            if not "id_planilla" in request.POST or request.session["idPorAprobar"] != int(request.POST["id_planilla"]):
                return redirectToError(request, "Ha ocurrido un error al procesar el ID de la planilla")
            # Si obtenemos el ID en el request, y coincide con el existente en la sesión, seguimos
            return aprobarPlanilla(request)
        if "id_planilla" in request.POST:
            return mostrarPlanillaAprobacion(request)
    return render(request, 'index.html')


def download_file(request):
    planillas = Planilla.objects.filter(id = request.session['id_planilla'])
    if len(planillas) != 1:
        return redirectToError(request, "No se ha encontrado la planilla")
    nombre_archivo = planillas[0].pdf_adjunto
    carpeta = "adjuntos/"
    fl_path = carpeta + nombre_archivo
    print(fl_path)
    try:
        fl = open(fl_path, "rb")
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % nombre_archivo
    except:
        return redirectToError(request, "No se ha encontrado el archivo adjunto")
    return response