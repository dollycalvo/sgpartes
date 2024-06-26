from partes.forms import FormSeleccionFecha
from partes.helper import tienePermisoEspecialEFL, tienePermisoEspecialRPA
from partes.models import FechasLimites, Planilla, Empleado, StatusPlanilla
from datetime import datetime
from django.shortcuts import render
from partes.views_helpers.common import nombresMeses, obtenerPlanillasParaRevisar


def cargarPlanillasParaMostrarYCalendario(request):
    fechaLimite = None
    fechaActual = datetime.now()
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    # Si la persona tiene el rol especial RPA (Revisión de Planillas Aprobadas), mostramos una tarjeta adicional
    rolRPA = None
    if (tienePermisoEspecialRPA(request.session['id_empleado'])):
        rolRPA = "RPA"
    rolEFL = None
    if (tienePermisoEspecialEFL(request.session['id_empleado'])):
        rolEFL = "EFL"
        # al tener permisos, cargamos también la fecha límite para mostrarlo
        fechaLimite = FechasLimites.objects.filter(mes = mesActual, anio = anioActual)        
        if len(fechaLimite) > 0:
            fechaLimite = fechaLimite[0]
        else:
            fechaLimite = 0
    form = FormSeleccionFecha()
    # Cargamos los datos para alimentar los filtros, excepto Borrador ya que el jefe directo no debería verlo
    statuses = StatusPlanilla.objects.filter(id__gt = 1)
    # Si no hay filtros aplicados, es porque entramos por GET y cargamos los filtros por defecto
    if "filtroEmpleado" not in request.POST:
        if rolRPA is not None:
            # Si es el rol RPA, ya filtramos por defecto el status 3 (Aprobado)
            filtros = {"empleado": 0, "mes": 0, "anio": 0, "status": 3}
        else:
            filtros = {"empleado": 0, "mes": 0, "anio": 0, "status": 2}
    else:
        filtros = {"empleado": request.POST["filtroEmpleado"],
                   "mes": request.POST["filtroMes"],
                   "anio": request.POST["filtroAnio"],
                   "status": request.POST["filtroStatus"]}
    # La listaSubordinados contiene la lista entera para mostrarlo en el filtro
    if rolRPA is not None or request.session['puesto'] == "Gerente":
        listaSubordinados = Empleado.objects.all().order_by("apellidos", "nombres")
    else:
        listaSubordinados = Empleado.objects.filter(jefe_directo = request.session['id_empleado']).order_by("apellidos", "nombres")
    if str(filtros["empleado"]) == "0":
        # Si no hay filtro, entonces buscamos las planillas de todos los empleados
        subordinados = listaSubordinados
    else:
        if rolRPA is not None or request.session['puesto'] == "Gerente":
            subordinados = Empleado.objects.get(id = int(filtros['empleado']))
        else:
            # Filtramos no sólo por id de empleado, sino también verificamos que pertenezca a nuestros subordinados, para evitar acceso a información no autorizada
            subordinados = Empleado.objects.get(id = int(filtros['empleado']), jefe_directo = request.session['id_empleado'])
    listaPlanillas = []
    soloIDsPlanillas = []
    # Recorremos la lista de subordinados (sean filtrados o no)
    for subordinado in subordinados:
        nombre_completo = subordinado.apellidos + ", " + subordinado.nombres
        planillasParaMostrar = Planilla.objects.filter(empleado = subordinado)
        # Continuamos los filtros si es que aplican
        if str(filtros["status"]) != "0":
            statusPlanillaFiltrado = StatusPlanilla.objects.filter(id = int(filtros["status"]))[0]
            planillasParaMostrar = planillasParaMostrar.filter(status = statusPlanillaFiltrado)
        else:
            # statusPlanillaFiltrado = StatusPlanilla.objects.filter(id__gt = 1)[0]
            planillasParaMostrar = planillasParaMostrar.filter(status_id__gt = 1)
        if str(filtros["mes"]) != "0":
            planillasParaMostrar = planillasParaMostrar.filter(mes = int(filtros["mes"]))
        if str(filtros["anio"]) != "0":
            planillasParaMostrar = planillasParaMostrar.filter(anio = int(filtros["anio"]))
        # Por último ordenamos
        planillasParaMostrar = planillasParaMostrar.order_by("anio", "mes", "status")
            
        if len(planillasParaMostrar) > 0:
            planillasDeEmpleado = {"id": subordinado.id,
                                "nombre_completo": nombre_completo,
                                "planillasParaMostrar": []
                                }
            for planilla in planillasParaMostrar:
                soloIDsPlanillas.append(planilla.id)
                planillasDeEmpleado["planillasParaMostrar"].append({"id": planilla.id,
                                                                   "mes": nombresMeses[int(planilla.mes) - 1],
                                                                   "anio": planilla.anio,
                                                                   "status": planilla.status.status})
            listaPlanillas.append(planillasDeEmpleado)
    # Guardamos la lista en la sesión para verificarla posteriormente al procesarla,
    # para evitar que un supervisor acceda a una planilla a la cual no está autorizado
    request.session['idsPlanillasParaMostrar'] = soloIDsPlanillas
        
    anios = list(range(anioActual - 3, anioActual + 2))
    mensaje = ""
    if "dashboard_mensaje" in request.session:
        mensaje = request.session['dashboard_mensaje']
        del request.session['dashboard_mensaje']
    planillasParaRevisar = obtenerPlanillasParaRevisar(request.session['id_empleado'])
    return render(request, 'dashboard.html', {"form": form, 
                                                "mensaje": mensaje,
                                                "anios": anios, 
                                                "nombresMeses": nombresMeses, 
                                                "mesActual": mesActual, 
                                                "anioActual": anioActual,
                                                "listaPlanillas": listaPlanillas,
                                                "listaSubordinados": listaSubordinados,
                                                "statuses": statuses,
                                                "filtros": filtros,
                                                "planillasParaRevisar": planillasParaRevisar,
                                                "rolRPA": rolRPA,
                                                "rolEFL": rolEFL,
                                                "fechaLimite": fechaLimite})
