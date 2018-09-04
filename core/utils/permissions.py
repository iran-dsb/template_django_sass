from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls.base import reverse_lazy


class is_superuser_or_in_role_mixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.groups.exists():
            return True
        return False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())

        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('')) # TODO página completar dados cadastrais
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class is_vendedor_mixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_vendedor:
            return True
        return False

class is_barqueiro_mixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_barqueiro:
            return True
        return False

class is_militante_mixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_militante:
            return True
        return False


def is_militante_check(user):
    if user.is_militante:
        return True
    return False