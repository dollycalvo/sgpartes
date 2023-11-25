import sqlite3
import datetime
import calendar
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

def ayuda(request):
    return render(request,'ayuda.html')

def planilla(request):
    id_agente = "1" # hard-coded, después lo cambio por el logueado
    mes = request.POST['mesReporte']
    anio = request.POST['anioReporte']
    dias_del_mes = range(1, calendar.monthrange(int(anio), int(mes))[1] + 1)
    try:
        conn = sqlite3.connect("soportes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT legajo, apellidos, nombres FROM agentes WHERE id_agente = ?", id_agente)
        datosAgente = cursor.fetchone()
        sqlParams = [id_agente, mes, anio]
        cursor.execute("""SELECT * FROM planilla WHERE id_agente = ? AND mes = ? AND año = ?""", sqlParams)
        datosPlanilla = cursor.fetchone()
        if datosPlanilla is not None:
            cursor.execute("SELECT * FROM registro_diario WHERE id_planilla = ?", datosPlanilla[0])
            datosDiarios = cursor.fetchall()
        else:
            datosPlanilla = [0, id_agente, mes, anio, False]
            datosDiarios = None
        templateParams = {  "datosAgente": datosAgente,
                            "datosPlanilla": datosPlanilla,
                            "datosDiarios": datosDiarios,
                            "mesReporte": nombresMeses[int(mes) - 1]["Nombre"],
                            "anioReporte": anio,
                            "diasDelMes": dias_del_mes}
        cursor.close()
    except sqlite3.Error as error:
        templateParams = None
        print("Han existido errores en la conexión a la base de datos", error)
    finally:
        if (conn):
            conn.close()
    return render(request, 'planilla.html', templateParams)

def seleccionfecha(request):
    fechaActual = datetime.datetime.now()
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    anios = list(range(anioActual - 3, anioActual + 2))
    return render(request, 'seleccionfecha.html', {"anios": anios, "nombresMeses": nombresMeses, "mesActual": mesActual, "anioActual": anioActual})

def login(request):
    if (request.GET.get('email') == "carlosguimaraenz@yahoo.com.ar"):
        return render(request,'index.html')
    else:
        return render(request,'ayuda.html')