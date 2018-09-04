import uuid
import re
import os
import io

from PIL import Image
from django.core.files.base import ContentFile

from django.utils import timezone


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    hoje = timezone.now()
    path = '{0}_{1}_fotos_uploads/{2}/{3}'.format(instance._meta.app_label.lower(), instance.__class__.__name__.lower(),
                                                      hoje.year, hoje.month)
    return os.path.join(path, filename)


def get_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    hoje = timezone.now()
    path = '{0}_{1}_thumbnails/{2}/{3}'.format(instance._meta.app_label.lower(), instance.__class__.__name__.lower(),
                                                      hoje.year, hoje.month)
    return os.path.join(path.lower(), filename)


def resize_image(img, max_size=900):
    original_w, original_h = img.size
    exif = None
    formato = img.format
    if 'exif' in img.info:
        exif = img.info['exif']

    new_size = scale_dimension(original_w, original_h, max_size=max_size)
    content = io.BytesIO()
    img = img.resize(new_size, Image.ANTIALIAS)

    #save the resized file to our IO ouput with the correct format and EXIF data ;-)
    if exif:
        img.save(content, format=formato, exif=exif, quality=90)
    else:
        img.save(content, format=formato, quality=90)

    return ContentFile(content.getvalue())


def scale_dimension(width, height, max_size):
    if width > height:
        ratio = max_size * 1. / width
    else:
        ratio = max_size * 1. / height
    return int(width * ratio), int(height * ratio)


def get_thumbnail(img, max_size=250):
    """
    Create and save the thumbnail for the photo (simple resize with PIL).
    """
    original_w, original_h = img.size
    new_size = scale_dimension(original_w, original_h, max_size=max_size)
    img.thumbnail(new_size, Image.ANTIALIAS)
    # Save thumbnail to in-memory file as BytesIO
    content = io.BytesIO()
    img.save(content, 'JPEG')
    return ContentFile(content.getvalue())