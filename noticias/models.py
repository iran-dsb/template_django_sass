from ckeditor_uploader.fields import RichTextUploadingField
from core.models.ModelBase import ModelBase, DeleteImagemThumbMixin
from core.utils.imagens import get_file_path, get_thumbnail_path
from django.db.models import CASCADE
from django.utils import timezone

from django.db import models
# Create your models here.
from noticias.queries import NoticiasQueryset
from taggit.managers import TaggableManager
from usuarios.models import Usuario
from image_cropping import ImageRatioField
import random


class Categoria(ModelBase):
    descricao = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(verbose_name='URL Amigável', unique=True)
    criado_por = models.ForeignKey(Usuario, related_name='categorias_noticia_criadas', default=1, on_delete=CASCADE)
    modificado_por = models.ForeignKey(Usuario, related_name='categorias_noticia_modificadas', null=True, on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('noticias.views.categoria_details', kwargs={'slug': self.slug})
        #return 'noticias:visualizar_categoria', (), {'slug': self.slug}

    class Meta:
        verbose_name = 'Categoria de Notícia'
        verbose_name_plural = 'Categorias de Notícia'
        ordering = ['descricao']


class Noticia(ModelBase):
    APROVADA = 1
    PARA_APROVACAO = 2
    EM_AUTORIA = 3

    STATUS_NOTICIA = [
        (APROVADA, 'Aprovada'),
        (PARA_APROVACAO, 'Para Aprovação'),
        (EM_AUTORIA, 'Em Autoria')
    ]

    DESTAQUE_1 = 1
    DESTAQUE_2 = 2
    DESTAQUE_3 = 3

    LOCAIS_DESTAQUE = [
        (DESTAQUE_1, 'Destaque 1'),
        (DESTAQUE_2, 'Destaque 2'),
        (DESTAQUE_3, 'Destaque 3'),
    ]

    data_publicacao = models.DateTimeField(verbose_name='Data de Publicação', default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='noticias')
    status = models.PositiveSmallIntegerField(choices=STATUS_NOTICIA, default=EM_AUTORIA)
    credito = models.CharField(verbose_name='Crédito', max_length=60, null=True, blank=True)
    fonte = models.CharField(max_length=60, null=True, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=120)
    subtitulo = models.CharField(verbose_name='Subtítulo', max_length=120, null=True, blank=True)
    slug = models.SlugField(verbose_name='URL Amigável', unique=True)
    resumo = models.TextField(max_length=600, blank=True, null=True)
    texto = RichTextUploadingField()
    tags = TaggableManager()
    destaque = models.PositiveSmallIntegerField(verbose_name='Local de Destaque',
                                                choices=LOCAIS_DESTAQUE,
                                                null=True,
                                                blank=True)
    data_destaque = models.DateTimeField(null=True, blank=True)

    criado_por = models.ForeignKey(Usuario, related_name='noticias_criadas', default=1, on_delete=CASCADE)
    modificado_por = models.ForeignKey(Usuario, related_name='noticias_modificadas', null=True, on_delete=CASCADE)
    aprovado_por = models.ForeignKey(Usuario, related_name='noticias_aprovadas', null=True, on_delete=CASCADE)
    aprovado_em = models.DateTimeField(null=True)

    @property
    def comentarios_aprovados(self):
        return self.comentarios.filter(status=Comentario.APROVADO)

    objects = NoticiasQueryset.as_manager()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('noticias.views.noticias_details', kwargs={'slug': self.slug})
        #return 'noticias:noticia', (), {'slug': self.slug}

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
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-data_publicacao', 'titulo']
        permissions = (
            ("aprovar_noticia", "Usuário pode aprovar uma notícia para exibir no portal"),
        )


class FotoNoticia(DeleteImagemThumbMixin, ModelBase):
    titulo = models.CharField(verbose_name='Título', max_length=120, blank=True, null=True)
    credito = models.CharField(verbose_name='Crédito', max_length=120, blank=True, null=True)
    descricao = models.CharField(verbose_name='Descrição', max_length=250, blank=True, null=True)
    imagem = models.ImageField(upload_to=get_file_path)
    imagem_thumbnail = models.ImageField(upload_to=get_thumbnail_path, null=True, blank=True)
    capa = models.BooleanField(default=False)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='imagens')

    def __str__(self):
        return self.titulo or ''

    class Meta:
        verbose_name = 'Foto Notícia'
        verbose_name_plural = 'Fotos Notícia'
        ordering = ['titulo']


class Comentario(ModelBase):
    EM_ANALISE = 1
    APROVADO = 2
    RECUSADO = 3
    STATUS_COMENTARIO = (
        (EM_ANALISE, 'Em Análise'),
        (APROVADO, 'Aprovado'),
        (RECUSADO, 'Recusado'),
    )
    nome = models.CharField(verbose_name='Nome', max_length=150)
    email = models.EmailField(verbose_name='E-mail')
    texto = models.TextField()
    status = models.IntegerField(choices=STATUS_COMENTARIO, default=EM_ANALISE)
    noticia = models.ForeignKey(Noticia, related_name='comentarios', on_delete=CASCADE)
    aprovado_em = models.DateTimeField(blank=True, null=True)
    aprovado_por = models.ForeignKey('usuarios.Usuario', null=True, related_name="comentarios_aprovacoes", on_delete=CASCADE)

    def __str__(self):
        return '{0} <{}> - {}'.format(self.nome, self.email, self.noticia.titulo)

    class Meta:
        verbose_name = 'Comentário Notícia'
        verbose_name_plural = 'Comentários Notícia'
        ordering = ['-created']
