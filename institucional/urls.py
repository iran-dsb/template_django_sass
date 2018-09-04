from django.urls import path

from .views import *

app_name = 'institucional'
urlpatterns = [
    path('', sobre, name='sobre'),
]
