from auditlog.models import AuditlogHistoryField
from core.utils.imagens import resize_image, get_thumbnail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
import itertools
import os
from PIL import Image

class ModelBase(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    history = AuditlogHistoryField()

    class Meta:
        abstract = True


class DeleteArquivoMixin():
    attr_arquivo = ['foto', 'logo', 'imagem', 'arquivo']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_file = self.__class__.objects.get(pk=self.pk)
            for attr in self.attr_arquivo:
                if getattr(old_file, attr, None) != getattr(self, attr, None):
                    file = getattr(old_file, attr, None)
                    if file:
                        file.delete(False)

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        for attr in self.attr_arquivo:
            file = getattr(self, attr, None)
            if file:
                file.delete(False)
        return super().delete(using, keep_parents)


class DeleteImagemThumbMixin():
    attr_arquivo = ['foto', 'logo', 'imagem', 'arquivo']
    IMG_DEFAULT_MAX_SIZE = 900
    THUMBNAIL_DEFAULT_MAX_SIZE = 250

    dict_max_size = {
        'foto': IMG_DEFAULT_MAX_SIZE,
        'logo': IMG_DEFAULT_MAX_SIZE,
        'imagem': IMG_DEFAULT_MAX_SIZE,
        'arquivo': IMG_DEFAULT_MAX_SIZE,
        'foto_thumbnail': THUMBNAIL_DEFAULT_MAX_SIZE,
        'logo_thumbnail': THUMBNAIL_DEFAULT_MAX_SIZE,
        'imagem_thumbnail': THUMBNAIL_DEFAULT_MAX_SIZE,
        'arquivo_thumbnail': THUMBNAIL_DEFAULT_MAX_SIZE,
    }

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_file = self.__class__.objects.get(pk=self.pk)
            for attr in self.attr_arquivo:
                if getattr(old_file, attr, None) != getattr(self, attr, None):
                    file = getattr(old_file, attr, None)
                    thumb = getattr(old_file, attr + '_thumbnail', None)
                    if thumb:
                        thumb.delete(False)
                    if file:
                        file.delete(False)
                    self.salvar_imagem_e_miniatura(attr)
        else:
            self.salvar_imagens_e_miniaturas()

        super().save(*args, **kwargs)

    def salvar_imagem_e_miniatura(self, attr):
        imagem = getattr(self, attr, None)
        if imagem:
            img = Image.open(imagem)
            self.set_file_name_ext()
            imagem.file = resize_image(img)
            thumb = getattr(self, attr+'_thumbnail', None)
            if thumb is not None:
                # Save image to a SimpleUploadedFile which can be saved into
                # ImageField
                suf = SimpleUploadedFile(os.path.split(imagem.name)[-1],
                                         get_thumbnail(img).read(),
                                         content_type='image/jpeg')
                # Save SimpleUploadedFile into image field
                thumb.save(imagem.name, suf, save=False)

    def salvar_imagens_e_miniaturas(self):
        for attr in self.attr_arquivo:
            imagem = getattr(self, attr, None)
            if imagem:
                img = Image.open(imagem)
                self.set_file_name_ext()
                imagem.file = resize_image(img, self.dict_max_size.get(attr, self.IMG_DEFAULT_MAX_SIZE))
                thumb = getattr(self, attr+'_thumbnail', None)
                if thumb is not None:
                    # Save image to a SimpleUploadedFile which can be saved into
                    # ImageField
                    suf = SimpleUploadedFile(os.path.split(imagem.name)[-1],
                                             get_thumbnail(img, self.dict_max_size.get(attr, self.THUMBNAIL_DEFAULT_MAX_SIZE)).read(),
                                             content_type='image/jpeg')
                    # Save SimpleUploadedFile into image field
                    thumb.save(imagem.name, suf, save=False)

    def delete(self, using=None, keep_parents=False):
        attr_arquivo_thumbnail = [a + '_thumbnail' for a in self.attr_arquivo]
        for attr in itertools.chain(self.attr_arquivo, attr_arquivo_thumbnail):
            file = getattr(self, attr, None)
            if file:
                file.delete(False)
        return super().delete(using, keep_parents)

    def set_file_name_ext(self, ext='jpg'):
        name = os.path.splitext(self.imagem.name)[0].lower()
        self.imagem.name = "%s.%s" % (name, ext)