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
    path('download/<int:eid>/<int:fid>/', views.download_file, name="download_file"),
    path('enviar_mail', views.enviar_mail, name="enviar_mail"),
    path('fecha_limite', views.recargar_fecha_limite, name="recargar_fecha_limite"),
    path('establecer_fecha_limite', views.establecer_fecha_limite, name="establecer_fecha_limite")
]