from django.db import models

class Puesto(models.Model):
    nombre = models.TextField()
    

class Empleado(models.Model):
    legajo = models.IntegerField()
    apellidos = models.TextField()
    nombres = models.TextField()
    puesto = models.ForeignKey(Puesto, on_delete=models.DO_NOTHING, default=None)
    jefe_directo = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING, default=None)
    email = models.TextField()
    password = models.CharField(max_length=100)
    

class StatusPlanilla(models.Model):
    status = models.TextField()


class Planilla(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, default=None)
    mes = models.SmallIntegerField(default=0)
    anio = models.SmallIntegerField(default=0)
    pdf_adjunto = models.TextField(default="")
    status = models.ForeignKey(StatusPlanilla, on_delete=models.DO_NOTHING, default=None)    


class RegistroDiario(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, default=None)
    dia = models.SmallIntegerField()
    codigo = models.CharField(max_length=3)
    observaciones = models.TextField()


class RegeneracionPW(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, default=None)
    codigo = models.CharField(max_length=64)
