from core.utils.paginacao import get_obj_paginado, get_query_string_to_pagination
from galerias.models import Galeria
from django.shortcuts import render, get_object_or_404


def galerias_list(request):
    template_name = 'galerias_list.html'

    galerias = Galeria.objects.publicadas()

    page = request.GET.get('page')
    qtd_pag = 9
    page_range, galerias = get_obj_paginado(page, qtd_pag, galerias)
    query_string = get_query_string_to_pagination(request)

    context = {
        'galerias': galerias,
        'page_range': page_range,
        'query_string': query_string,
    }

    return render(request, template_name, context)


def galerias_details(request, slug):
    template_name = 'galerias_details.html'
    galeria = get_object_or_404(Galeria.objects.publicadas(), slug=slug)
    context = {
        'galeria': galeria,
    }
    return render(request, template_name, context)