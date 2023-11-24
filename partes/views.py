import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    # return HttpResponse("<h1>Bienvenido al sistema SGPARTES</h1>")
    return render(request, 'index.html');

def ayuda(request):
    return render(request,'ayuda.html')

def seleccionfecha(request):
    fechaActual = datetime.datetime.now()
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
    mesActual = fechaActual.month
    anioActual = fechaActual.year
    anios = list(range(anioActual - 3, anioActual + 2))
    return render(request, 'seleccionfecha.html', {"anios": anios, "nombresMeses": nombresMeses, "mesActual": mesActual, "anioActual": anioActual})

def login(request):
    if (request.GET.get('email') == "carlosguimaraenz@yahoo.com.ar"):
        return render(request,'index.html')
    else:
        return render(request,'ayuda.html')