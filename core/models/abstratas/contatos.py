from django.db import models

class ContatoModel(models.Model):
    telefone = models.CharField('Telefone', max_length=16, null=True, blank=True)
    celular = models.CharField('Celular', max_length=16, null=True, blank=True)
    email = models.EmailField('E-mail', max_length=200, null=True, blank=True)

    class Meta:
        abstract = True