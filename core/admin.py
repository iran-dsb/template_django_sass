from core.models.enderecos import *
from django.contrib import admin

# Register your models here.


class BaseModelCreatedAndChangedFieldsAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            obj.modificado_por = request.user
        else:
            obj.criado_por = request.user

        super().save_model(request, obj, form, change)


class PermissionFieldMixin(object):
    def get_form(self, request, obj=None, **kwargs):
        if hasattr(self, 'field_permissions'):
            user = request.user
            for _field in self.opts.fields:
                perm = self.field_permissions.get(_field.name)
                if perm and not user.has_perm(perm):
                    if self.exclude:
                        self.exclude.append(_field.name)
                    else:
                        self.exclude = [_field.name]
        return super().get_form(request, obj, **kwargs)

admin.site.register(Regiao)
admin.site.register(Estado)
admin.site.register(Mesorregiao)
admin.site.register(Microrregiao)
admin.site.register(Municipio)
admin.site.register(Bairro)