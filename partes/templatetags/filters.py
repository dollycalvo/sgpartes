from django import template
from partes.helper import diasDeLaSemana, etiquetaCodigo

register = template.Library()

@register.filter
def etiqueta_codigo(value):
    """Convierte el código en una etiqueta para el usuario"""
    return etiquetaCodigo(value)


@register.filter
def dia_semana(dia, primerDiaDelMes):
    """Devuelve el día de la semana en base al comienzo y al número de día dado"""
    return diasDeLaSemana[((dia - 1) + primerDiaDelMes) % 7]["corto"]
