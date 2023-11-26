import sqlite3
import datetime
import calendar
from partes.models import Agentes, Planilla, RegistroDiario
from partes.forms import FormSeleccionFecha
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse

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
    print(request.method)
    acciones_submit = ['guardar', 'presentar']
    id_agente = "1" # hard-coded, después lo cambio por el logueado
    if request.method == "POST":
        print(request.POST['accion_submit'])
        mes = request.POST['mesReporte']
        anio = request.POST['anioReporte']
    else:
        accion_submit = acciones_submit[0]
        if not 'mesReporte' in request.session:
            return HttpResponseRedirect("/error")
        mes = request.session['mesReporte']
        anio = request.session['anioReporte']
        del request.session['mesReporte']
        del request.session['anioReporte']
        dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
    datosAgente = Agentes.objects.filter(id=id_agente)
    datosPlanilla = Planilla.objects.filter(agente_id=id_agente, mes=mes, anio=anio)
    if len(datosPlanilla) == 1:
        datosDiarios = RegistroDiario.objects.filter(planilla_id=datosPlanilla[0].id)
    else:
        datosPlanilla = [0, id_agente, mes, anio, False]
        datosDiarios = None
    templateParams = {  "accion_submit": accion_submit,
                        "acciones_submit": acciones_submit[0] + "#" + acciones_submit[1],
                        "datosAgente": datosAgente[0],
                        "datosPlanilla": datosPlanilla,
                        "datosDiarios": datosDiarios,
                        "mesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                        "anioReporte": anio,
                        "diasDelMes": dias_del_mes}
    return render(request, 'planilla.html', templateParams)



def seleccionfecha(request):
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
    if (request.GET.get('email') == "carlosguimaraenz@yahoo.com.ar"):
        return render(request,'index.html')
    else:
        return render(request,'ayuda.html')
    
    

def error(request):
    return render(request, 'error.html')