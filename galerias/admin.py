from core.admin import BaseModelCreatedAndChangedFieldsAdmin
from django.contrib import admin

# Register your models here.
from galerias.forms import GaleriaForm
from galerias.models import *
from django.utils import timezone


class FotoGaleriaTabularAdmin(admin.StackedInline):
    model = FotoGaleria
    exclude = ['imagem_thumbnail']


class GaleriaAdmin(BaseModelCreatedAndChangedFieldsAdmin):
    def data_publicacao_formated(self, obj):
        if obj.data_publicacao:
            return timezone.localtime(obj.data_publicacao).strftime("%d/%m/%Y %H:%M:%S")
        return '-'

    data_publicacao_formated.short_description = 'Data de Publicação'

    list_display = ['titulo', 'data_publicacao_formated', 'ativa', 'criado_por']
    search_fields = ['titulo']
    list_editable = ['ativa']
    list_filter = ['ativa', 'data_publicacao']

    prepopulated_fields = {'slug': ('titulo',)}
    form = GaleriaForm

    #field_permissions = {'status': 'galerias.aprovar_galeria'}

    inlines = [
        FotoGaleriaTabularAdmin
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form


admin.site.register(Galeria, GaleriaAdmin)
