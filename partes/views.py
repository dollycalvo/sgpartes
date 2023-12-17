from partes.views_helper import (
    view_planilla,
    view_seleccionfecha,
    view_login,
    view_error,
    view_regenerar,
    view_dashboard,
    view_aprobar,
    view_downloadFile
)


def inicio(request):
    return login(request)


def planilla(request):    
    return view_planilla(request)


def seleccionfecha(request):
    return view_seleccionfecha(request)


def login(request):
    return view_login(request)    


def error(request):
    return view_error(request)


def regenerar(request):
    return view_regenerar(request)


def dashboard(request):
    return view_dashboard(request)


def aprobar(request):
    return view_aprobar(request)


def download_file(request):
    return view_downloadFile(request)
