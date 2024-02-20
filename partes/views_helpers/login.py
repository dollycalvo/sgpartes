from partes.helper import tienePermisosEspecialesParaDashboard
from partes.models import Empleado
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.shortcuts import render


def procesarLogout(request):
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
    if 'idsPlanillasParaMostrar' in request.session:
        del request.session['idsPlanillasParaMostrar']
    mensaje = "La sesión se ha cerrado correctamente"
    return mensaje


def buscarUsuario(request, MAX_LOGINS_INCORRECTOS):
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
            if empleados[0].puesto.nombre == "Agente" and not tienePermisosEspecialesParaDashboard(empleados[0].id):
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
