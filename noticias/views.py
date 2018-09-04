from core.utils.paginacao import get_obj_paginado, get_query_string_to_pagination
from django.db.models.aggregates import Count

from noticias.models import Noticia, Categoria
from django.shortcuts import render, get_object_or_404


def noticias_list(request, categoria=None, tag=None):
    template_name = 'noticias_list.html'

    if categoria:
        categoria = get_object_or_404(Categoria, slug=categoria)
        noticias = Noticia.objects.publicadas_categoria(categoria)
    elif tag:
        tags = tag.split("/")
        noticias = Noticia.objects.publicadas_tags(tags)
    else:
        noticias = Noticia.objects.publicadas()

    page = request.GET.get('page')
    qtd_pag = 20
    page_range, noticias = get_obj_paginado(page, qtd_pag, noticias)
    query_string = get_query_string_to_pagination(request)

    context = {
        'noticias': noticias,
        'categorias': Categoria.objects.filter(noticias__isnull=False).distinct(),
        'ultimas_noticias': Noticia.objects.get_ultimas(),
        'page_range': page_range,
        'query_string': query_string,
        'list_anim': ['left', 'right', 'bottom']
    }

    return render(request, template_name, context)


def noticias_search(request):
    template_name = 'noticias_list.html'

    busca = request.GET.get('search', '')

    noticias = Noticia.objects.publicadas().filter(titulo__icontains=busca)

    page = request.GET.get('page')
    qtd_pag = 20
    page_range, noticias = get_obj_paginado(page, qtd_pag, noticias)
    query_string = get_query_string_to_pagination(request)

    context = {
        'noticias': noticias,
        'categorias': Categoria.objects.filter(noticias__isnull=False).distinct(),
        'ultimas_noticias': Noticia.objects.get_ultimas(),
        'page_range': page_range,
        'query_string': query_string
    }

    return render(request, template_name, context)



def noticias_details(request, slug):
    template_name = 'noticias_details.html'
    noticia = get_object_or_404(Noticia.objects.publicadas(), slug=slug)
    link_dominio = "http://%s" % request.META['HTTP_HOST']
    context = {
        'link_dominio': link_dominio,
        'noticia': noticia,
        'categorias': Categoria.objects.filter(noticias__isnull=False).distinct(),
        'ultimas_noticias': Noticia.objects.get_ultimas(),
    }
    return render(request, template_name, context)
