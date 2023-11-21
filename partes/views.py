from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    return HttpResponse("<h1>Bienvenido al sistema SGPARTES</h1>")

def ayuda(request):
    return render(request,'ayuda.html')

