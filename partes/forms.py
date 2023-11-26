from django import forms

class FormSeleccionFecha(forms.Form):
    mesReporte = forms.IntegerField(label = "Mes:")
    anioReporte = forms.IntegerField(label = "Año:")
