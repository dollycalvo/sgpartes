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
    

class PermisoEspecial(models.Model):
    codigo = models.TextField(null=False, default="")
    nombre = models.TextField(null=False, default="")
    descripcion = models.TextField(null=True, default="")
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, default=None)
    

class StatusPlanilla(models.Model):
    status = models.TextField()


class Planilla(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, default=None)
    mes = models.SmallIntegerField(default=0)
    anio = models.SmallIntegerField(default=0)
    status = models.ForeignKey(StatusPlanilla, on_delete=models.DO_NOTHING, default=None)
    observaciones = models.TextField(default="")
    
    
class Adjuntos(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, default=None)
    nombre_archivo = models.TextField(default="")


class RegistroDiario(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, default=None)
    dia = models.SmallIntegerField()
    codigo = models.CharField(max_length=3)
    observaciones = models.TextField(default="")


class RegeneracionPW(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, default=None)
    codigo = models.CharField(max_length=64)


class FechasLimites(models.Model):
    mes = models.SmallIntegerField(default=0)
    anio = models.SmallIntegerField(default=0)
    diaLimite = models.SmallIntegerField(default=0)


class TipoCambio(models.Model):
    nombre = models.TextField(default="")
    
    
class CampoHistorial(models.Model):
    nombre = models.TextField(default="")
    
    
class RegistroHistorial(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, default=None)
    fechaHora = models.DateTimeField()
    tipo = models.ForeignKey(TipoCambio, on_delete=models.DO_NOTHING, default=None)
    campo = models.ForeignKey(CampoHistorial, on_delete=models.DO_NOTHING, default=None)
    diaCambio = models.TextField(default="")    # En caso de que el cambio sea en código u observación, se usará este campo
    anterior = models.TextField(default="")
    nuevo = models.TextField(default="")