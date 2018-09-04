from django import forms
from noticias.models import Noticia


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['data_publicacao', 'titulo', 'subtitulo', 'slug', 'categoria', 'status', 'credito', 'fonte', 'destaque',
                  'data_destaque', 'resumo', 'texto', 'tags']

    def clean_data_destaque(self):
        destaque = self.cleaned_data['destaque']
        data_destaque = self.cleaned_data['data_destaque']
        if destaque and not data_destaque:
            self.add_error('data_destaque', 'Este campo é obrigatório, quando selecionar um destaque')
        return data_destaque

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user and not self.user.has_perm('noticias.aprovar_noticia'):
            self.fields['status'].choices = [c for c in self.fields['status'].choices if c[0] != Noticia.APROVADA]


class NoticiaChangeListForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['status', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user and not self.user.has_perm('noticias.aprovar_noticia'):
            self.fields['status'].choices = [c for c in self.fields['status'].choices if c[0] != Noticia.APROVADA]



