from partes.models import Empleado, RegeneracionPW
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render
import hashlib
from datetime import datetime


def generarCodigo(request, acciones):
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



def crearNuevoPassword(request, acciones):
    MAX_ERRORES = 2
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
