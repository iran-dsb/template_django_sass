from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from usuarios.models import Usuario


class UsuarioCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar a Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nome', 'username', 'is_admin', 'is_active')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas estão diferentes.")
        return password2

    def save(self, commit=True):

        user = super(UsuarioCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('nome', 'username', 'password', 'is_active', 'is_admin')

    def clean_password(self):

        return self.initial["password"]


class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ['username', 'nome', 'is_active', 'is_admin']
    list_filter = ('is_active',)
    search_fields = ('username', 'nome')
    ordering = ('nome',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_active', 'is_admin', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'username', 'password1', 'password2',),
        }),
    )
admin.site.register(Usuario, UsuarioAdmin)
