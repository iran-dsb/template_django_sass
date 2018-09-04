from django.urls import path

from .views import *
app_name = 'contato'
urlpatterns = [
    path('', ContatoView.as_view(), name='contato'),
]
