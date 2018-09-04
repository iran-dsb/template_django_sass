from core.models.ModelBase import ModelBase
from django.db import models

# Create your models here.


class Mensagem(ModelBase):
    nome = models.CharField(verbose_name='Nome', max_length=100)
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(verbose_name='Telefone', max_length=16)
    assunto = models.CharField(max_length=200, blank=True)
    mensagem = models.TextField()

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.nome, self.email, self.assunto)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-created']
