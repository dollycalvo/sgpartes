from partes.forms import FormSeleccionFecha
from partes.models import Planilla, Empleado, StatusPlanilla
from datetime import datetime
from django.shortcuts import render
from partes.views_helpers.common import nombresMeses


def cargarPlanillasPorAprobarYCalendario(request):
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
