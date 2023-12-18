from django.http import HttpResponseRedirect

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


def redirectToError(request, mensaje):
    request.session["mensaje_error"] = mensaje
    return HttpResponseRedirect("/error")
