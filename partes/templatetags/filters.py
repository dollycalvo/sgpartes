from django import template
from partes.helper import diasDeLaSemana, etiquetaCodigo
from partes.views_helpers.common import DIA_LIMITE_PRESENTACION_PLANILLA

register = template.Library()

@register.filter
def etiqueta_codigo(value):
    """Convierte el código en una etiqueta para el usuario"""
    return etiquetaCodigo(value)


@register.filter
def dia_semana(dia, primerDiaDelMes):
    """Devuelve el día de la semana en base al comienzo y al número de día dado"""
    return diasDeLaSemana[((dia - 1) + primerDiaDelMes) % 7]["corto"]


@register.filter
def class_dia_semana(dia, primerDiaDelMes):
    """Devuelve una clase CSS de acuerdo al día de la semana en base al comienzo y al número de día dado"""
    diaSemana = ((dia - 1) + primerDiaDelMes) % 7
    return "dia-finde" if diaSemana >= 5 else "dia-semana"


@register.filter
def concat(txt1, txt2):
    """Concatena dos strings"""
    return str(txt1) + str(txt2)


@register.filter
def concatDiaLimite(txt1):
    """Concatena dos strings"""
    return str(txt1) + str(DIA_LIMITE_PRESENTACION_PLANILLA)