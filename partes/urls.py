from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('seleccionfecha', views.seleccionfecha, name='seleccionfecha'),
    path('login', views.login, name='login'),
    path('planilla', views.planilla, name="planilla"),
    path('error', views.error, name="error"),
    path('regenerar', views.regenerar, name="regenerar"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('aprobar', views.aprobar, name="aprobar"),
    path('download', views.download_file, name="download_file")
]