from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Usuário deve ter um nome de usuário válido.')

        usuario = self.model(
            username=self.model.normalize_username(username)
        )

        usuario.set_password(password)
        usuario.save()

        return usuario

    def create_superuser(self, username, password, **kwargs):
        usuario = self.create_user(username, password, **kwargs)

        usuario.is_admin = True
        usuario.is_superuser = True
        usuario.save()

        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, verbose_name="Nome de usuário")
    nome = models.CharField(max_length=40)
    is_admin = models.BooleanField(default=False, verbose_name="É Administrador")
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nome']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome
