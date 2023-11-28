from django import template

register = template.Library()

@register.filter
def etiqueta_codigo(value):
    """Convierte el código en una etiqueta para el usuario"""
    if value == "sn":
        return "S/N"
    if value == "cs":
        return "CS"
    if value == "v":
        return "V"
    if value == "sa":
        return "SA"
    return value