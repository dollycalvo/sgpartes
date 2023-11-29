from django.db import models

# Create your models here.
class Agentes(models.Model):
    legajo = models.IntegerField()
    apellidos = models.TextField()
    nombres = models.TextField()
    email_agente = models.TextField()
    jefe_directo = models.TextField()
    email_jefe_directo = models.TextField()
    password = models.CharField(max_length=100)
    
class Planilla(models.Model):
    agente = models.ForeignKey(Agentes, on_delete=models.DO_NOTHING, default=None)
    mes = models.SmallIntegerField(default=0)
    anio = models.SmallIntegerField(default=0)
    presentado = models.BooleanField(default=False)

class RegistroDiario(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, default=None)
    dia = models.SmallIntegerField()
    codigo = models.CharField(max_length=3)
    observaciones = models.TextField()

class RegeneracionPW(models.Model):
    agente = models.ForeignKey(Agentes, on_delete=models.DO_NOTHING, default=None)
    codigo = models.CharField(max_length=64)
