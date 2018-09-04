import uuid
import re
import os
# import io
#
# from PIL import Image
# from django.core.files.base import ContentFile

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def get_query_string_to_pagination(request, page_str='page'):
    query_string = request.META.get('QUERY_STRING')
    query_string = re.sub(r'(?i)&?(' + page_str + '=)(\d+)', '', query_string)
    if query_string:
        query_string += '&'
    return query_string


def get_obj_paginado(pagina, qtd_pagina, objects_list):
    paginator = Paginator(objects_list, qtd_pagina)
    try:
        objects_list = paginator.page(pagina)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)
    index = paginator.page_range.index(objects_list.number)
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = paginator.page_range[start_index:end_index]
    return page_range, objects_list


# def resize_image(img, max_size=900):
#     original_w, original_h = img.size
#     exif = None
#     formato = img.format
#     if 'exif' in img.info:
#         exif = img.info['exif']
#
#     new_size = scale_dimension(original_w, original_h, max_size=max_size)
#     content = io.BytesIO()
#     img = img.resize(new_size, Image.ANTIALIAS)
#
#     #save the resized file to our IO ouput with the correct format and EXIF data ;-)
#     if exif:
#         img.save(content, format=formato, exif=exif, quality=90)
#     else:
#         img.save(content, format=formato, quality=90)
#
#     return ContentFile(content.getvalue())
#
#
# def scale_dimension(width, height, max_size):
#     if width > height:
#         ratio = max_size * 1. / width
#     else:
#         ratio = max_size * 1. / height
#     return int(width * ratio), int(height * ratio)
#
#
# def get_thumbnail(img, max_size=250):
#     """
#     Create and save the thumbnail for the photo (simple resize with PIL).
#     """
#     original_w, original_h = img.size
#     new_size = scale_dimension(original_w, original_h, max_size=max_size)
#     img.thumbnail(new_size, Image.ANTIALIAS)
#     # Save thumbnail to in-memory file as BytesIO
#     content = io.BytesIO()
#     img.save(content, 'JPEG')
#     return ContentFile(content.getvalue())