from django.urls import path

from .views import *

app_name = 'galerias'
urlpatterns = [
    path('', galerias_list, name='galerias_list'),
    path('<slug:slug>/', galerias_details, name='galeria'),
]
