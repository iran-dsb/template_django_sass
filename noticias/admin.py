from core.admin import BaseModelCreatedAndChangedFieldsAdmin, PermissionFieldMixin
from core.admin_utils import status_aprovado_update
from django.contrib import admin

# Register your models here.
from image_cropping import ImageCroppingMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from noticias.forms import NoticiaForm, NoticiaChangeListForm
from noticias.models import *


class FotoNoticiaTabularAdmin(ImageCroppingMixin, admin.StackedInline):
    model = FotoNoticia
    exclude = ['imagem_thumbnail']


class CategoriaAdmin(BaseModelCreatedAndChangedFieldsAdmin):
    list_display = ['descricao', 'criado_por', 'created', 'modificado_por', 'modified']
    search_fields = ['descricao']
    exclude = ['criado_por', 'modificado_por']
    prepopulated_fields = {'slug': ('descricao',)}


class NoticiaAdmin(PermissionFieldMixin, BaseModelCreatedAndChangedFieldsAdmin):

    def data_publicacao_formated(self, obj):
        if obj.data_publicacao:
            return timezone.localtime(obj.data_publicacao).strftime("%d/%m/%Y %H:%M:%S")
        return '-'

    def data_aprovacao_formated(self, obj):
        if obj.aprovado_em:
            return timezone.localtime(obj.aprovado_em).strftime("%d/%m/%Y %H:%M:%S")
        return '-'

    data_publicacao_formated.short_description = 'Data de Publicação'
    data_aprovacao_formated.short_description = 'Aprovado Em'

    list_display = ['titulo', 'data_publicacao_formated', 'categoria', 'status', 'criado_por', 'aprovado_por',
                    'data_aprovacao_formated']
    search_fields = ['titulo']
    list_editable = ['status']
    list_filter = ['categoria', 'status', 'data_publicacao']

    prepopulated_fields = {'slug': ('titulo',)}
    form = NoticiaForm

    #field_permissions = {'status': 'noticias.aprovar_noticia'}

    inlines = [
        FotoNoticiaTabularAdmin
    ]

    def save_model(self, request, obj, form, change):
        status_aprovado_update(change, form, obj, Noticia.APROVADA)
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
            Método para redirecionar para listagem, caso o usuário não tenha acesso à edição do registro
            sem esse método ao acessar a URL de edição diretamente resulta em 404,
            pois já está bloqueado pelo get_queryset.
        """
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse(
                'admin:noticias_noticia_changelist'))
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm('noticias.aprovar_noticia'):
            return qs
        return qs.exclude(status=Noticia.APROVADA)

    def get_changelist_form(self, request, **kwargs):
        kwargs['form'] = NoticiaChangeListForm
        form = super().get_changelist_form(request, **kwargs)
        form.user = request.user
        return form


class ComentarioAdmin(admin.ModelAdmin):

    list_display = ['nome', 'email', 'status', 'aprovado_em', 'aprovado_por']
    readonly_fields = [
        'nome', 'email', 'texto', 'noticia',
        'created', 'aprovado_em', 'aprovado_por'
    ]
    exclude = ['modified']
    search_fields = ['nome', 'email', 'noticia__titulo']


    def save_model(self, request, obj, form, change):
        status_aprovado_update(change, form, obj, Comentario.APROVADO)
        super().save_model(request, obj, form, change)



admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Comentario, ComentarioAdmin)
