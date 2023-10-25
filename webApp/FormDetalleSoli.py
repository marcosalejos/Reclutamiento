from django import forms

class FormularioDetalleSoli(forms.Form):

    FechaRevisada = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Comentarios = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )