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
        return "LAR"
    if value == "sa":
        return "SA"
    if value == "+":
        return "+"
    if value == "d":
        return "D"
    if value == "e":
        return "E"
    if value == "h":
        return "H"
    if value == "L":
        return "L"
    if value == "h":
        return "M"
    if value == "n":
        return "N"
    if value == "p":
        return "P"
    if value == "r":
        return "R"
    if value == "W":
        return "W"
    if value == "y":
        return "Y"
    if value == "z":
        return "Z"
    if value == "fr":
        return "FR"
    if value == "ja":
        return "JA"
    if value == "jh":
        return "JH"
    if value == "zd":
        return "ZD"
    if value == "cmp":
        return "CMP"
    if value == "cmt":
        return "CMT"
    if value == "cse":
        return "CSE"
    if value == "ff1":
        return "FF1"
    if value == "ff2":
        return "FF2"
    if value == "jlm":
        return "JLM"
    if value == "mex":
        return "MEX"
    if value == "qti":
        return "QTI"
    if value == "qco":
        return "QCO"
    if value == "qre":
        return "QRE"
    if value == "vre":
        return "VRE"
    if value == "x":
        return "X"
    if value == "unp":
        return "UNP"
    if value == "unt":
        return "UNT"
    if value == "unu":
        return "UNU"

    return value