from django.db import models
from django.db.models import CASCADE


class Regiao(models.Model):
    descricao = models.CharField('Descrição', max_length=100)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'
        ordering = ['id']


class Estado(models.Model):
    codigo = models.CharField('Código', max_length=5)
    descricao = models.CharField('Descrição', max_length=100)
    sigla = models.CharField('Sigla', max_length=2)
    regiao = models.ForeignKey(Regiao, related_name='estados', on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['descricao']


class Mesorregiao(models.Model):
    codigo = models.CharField('Código', max_length=5)
    descricao = models.CharField('Descrição', max_length=100)
    estado = models.ForeignKey(Estado, related_name='mesorregioes', on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Mesorregião'
        verbose_name_plural = 'Mesorregiões'
        ordering = ['descricao']


class Microrregiao(models.Model):
    codigo = models.CharField('Código', max_length=5)
    descricao = models.CharField('Descrição', max_length=100)
    mesorregiao = models.ForeignKey(Mesorregiao, related_name='microrregioes', on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Microrregião'
        verbose_name_plural = 'Microrregiões'
        ordering = ['descricao']

class Municipio(models.Model):
    descricao = models.CharField('Descrição', max_length=100)
    codigo = models.CharField('Código', max_length=5)
    codigo_completo = models.CharField('Código Completo', max_length=10)
    microrregiao = models.ForeignKey(Microrregiao, related_name='municipios', on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'
        ordering = ['descricao']


class Bairro(models.Model):
    codigo = models.CharField('Código', max_length=5)
    descricao = models.CharField('Descrição', max_length=100)
    municipio = models.ForeignKey(Municipio, related_name='bairros', on_delete=CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
        ordering = ['descricao']