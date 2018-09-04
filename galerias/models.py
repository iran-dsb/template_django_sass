from ckeditor.fields import RichTextField
from core.models.ModelBase import ModelBase, DeleteImagemThumbMixin
from core.utils.imagens import get_thumbnail_path, get_file_path
from django.db import models

# Create your models here.
from galerias.queries import GaleriasQueryset, FotoGaleriaQueryset
from usuarios.models import Usuario
import random
from django.utils import timezone


class Galeria(ModelBase):
    data_publicacao = models.DateTimeField(verbose_name='Data de Publicação', default=timezone.now)
    ativa = models.BooleanField(default=True)
    titulo = models.CharField(verbose_name='Título', max_length=120)
    slug = models.SlugField(verbose_name='URL Amigável', unique=True)
    texto = RichTextField()
    pousada = models.BooleanField('Fotos da pousada', default=False)


    criado_por = models.ForeignKey(Usuario, related_name='galerias_criadas', default=1, on_delete=models.CASCADE)
    modificado_por = models.ForeignKey(Usuario, related_name='galerias_modificadas', null=True, on_delete=models.CASCADE)

    objects = GaleriasQueryset.as_manager()

    @models.permalink
    def get_absolute_url(self):
        return 'galerias:galeria', (), {'slug': self.slug}

    @property
    def capa(self):
        try:
            imgs = [i for i in self.imagens.all() if i.capa] or [i for i in self.imagens.all()]
            return random.choice(imgs)
        except IndexError:
            return None

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galerias'
        ordering = ['-data_publicacao', 'titulo']


class FotoGaleria(DeleteImagemThumbMixin, ModelBase):
    titulo = models.CharField(verbose_name='Título', max_length=120)
    descricao = models.CharField(verbose_name='Descrição', max_length=250, blank=True, null=True)
    imagem = models.ImageField(upload_to=get_file_path)
    imagem_thumbnail = models.ImageField(upload_to=get_thumbnail_path, null=True, blank=True)
    capa = models.BooleanField(default=False)
    galeria = models.ForeignKey(Galeria, on_delete=models.CASCADE, related_name='imagens')
    credito = models.CharField(verbose_name='Crédito', max_length=120, blank=True, null=True)

    objects = FotoGaleriaQueryset.as_manager()

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Foto Galeria'
        verbose_name_plural = 'Fotos Galeria'
        ordering = ['titulo']