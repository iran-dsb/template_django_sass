from django.urls import path

from .views import *
app_name = 'noticias'
urlpatterns = [
    path('', noticias_list, name='noticias_list'),
    path('busca/', noticias_search, name='buscar'),
    path('tag/<slug:tag>/', noticias_list, name='noticias_list_tags'),
    path('categoria/<slug:categoria>/', noticias_list, name='noticias_list_categ'),
    path('<slug:slug>/', noticias_details, name='noticia'),
]
