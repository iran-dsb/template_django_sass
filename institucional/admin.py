from core.admin import BaseModelCreatedAndChangedFieldsAdmin
from django.contrib import admin

# Register your models here.
from institucional.models import Sobre


class SobreAdmin(BaseModelCreatedAndChangedFieldsAdmin):
    list_display = ['criado_por', 'created', 'modificado_por', 'modified']
    exclude = ['criado_por', 'modificado_por']

    fieldsets = (
        (None, {
            'fields': ('sobre', )
        }),
        ('Endereço', {
            'fields': ('logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'cep', 'uf'),
        }),
        ('Contato', {
            'fields': ('telefone', 'telefone_2', 'celular', 'email', ),
        }),
        ('Social', {
            'fields': ('twitter', 'facebook', 'instagram', 'youtube'),
        })
    )

admin.site.register(Sobre, SobreAdmin)
