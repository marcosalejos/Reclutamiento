from django import forms
import pyodbc


class FormularioObservaciones(forms.Form):

    Descripcion = forms.CharField(widget=forms.Textarea, required=True)
