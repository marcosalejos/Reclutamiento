from django import forms


class FormularioObservaciones(forms.Form):

    Descripcion = forms.CharField(widget=forms.Textarea, required=True)
