from django import forms
from galerias.models import Galeria


class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = ['data_publicacao', 'ativa', 'titulo', 'slug', 'texto', 'pousada']