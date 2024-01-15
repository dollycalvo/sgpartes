from django.http import HttpResponseRedirect

from partes.models import Planilla

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


def obtenerNombreMes(numeroMes):
    return nombresMeses[numeroMes - 1]["Nombre"]


def redirectToError(request, mensaje):
    request.session["mensaje_error"] = mensaje
    return HttpResponseRedirect("/error")


# Esta función devuelve las planillas para revisar para el empleado dado
def obtenerPlanillasParaRevisar(id_empleado):
    planillas = Planilla.objects.filter(empleado_id = id_empleado, status_id = 1).exclude(observaciones = "").order_by("anio", "mes")
    listaPlanillas = []
    for planilla in planillas:
        listaPlanillas.append({"id": planilla.id, "mes": obtenerNombreMes(planilla.mes), "anio": planilla.anio, "observaciones": planilla.observaciones})
    return listaPlanillas