from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    # return HttpResponse("<h1>Bienvenido al sistema SGPARTES</h1>")
    return render(request, 'index.html');

def ayuda(request):
    return render(request,'ayuda.html')

def seleccionfecha(request):
    return render(request, 'seleccionfecha.html')

def login(request):
    if (request.GET.get('email') == "carlosguimaraenz@yahoo.com.ar"):
        return render(request,'index.html')
    else:
        return render(request,'ayuda.html')