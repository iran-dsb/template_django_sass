from django import template

register = template.Library()


@register.inclusion_tag('paginacao.html')
def paginador(objects_list, page_range_obj, query_string, *args, **kwargs):
    page_str = kwargs.get('page_str', 'page')
    return {
        'objects_list': objects_list,
        'page_range_obj': page_range_obj,
        'query_string': query_string,
        'page_str': page_str,
    }