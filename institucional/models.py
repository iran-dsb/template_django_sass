from ckeditor.fields import RichTextField
from core.models.ModelBase import ModelBase
from django.db import models

# Create your models here.
from usuarios.models import Usuario

from enum import Enum, unique

@unique
class Uf(Enum):
    AC = 'Acre'
    AL = 'Alagoas'
    AP = 'Amapá'
    AM = 'Amazonas'
    BA = 'Bahia'
    CE = 'Ceará'
    DF = 'Distrito Federal'
    ES = 'Espírito Santo'
    GO = 'Goiás'
    MA = 'Maranhão'
    MT = 'Mato Grosso'
    MS = 'Mato Grosso do Sul'
    MG = 'Minas Gerais'
    PR = 'Paraná'
    PB = 'Paraíba'
    PA = 'Pará'
    PE = 'Pernambuco'
    PI = 'Piauí'
    RJ = 'Rio de Janeiro'
    RN = 'Rio Grande do Norte'
    RS = 'Rio Grande do Sul'
    RO = 'Rondônia'
    RR = 'Roraima'
    SC = 'Santa Catarina'
    SE = 'Sergipe'
    SP = 'São Paulo'
    TO = 'Tocantins'

    @classmethod
    def choices(cls):
        # ''' Método para facilitar o uso do choices no django, no momento está da forma mais complexa por motivos de
        # testes '''
        # # get all members of the class
        # members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # # filter down to just properties
        # props = [m for m in members if not(m[0][:2] == '__')]
        # # format into django choice tuple
        # choices = tuple([(str(p[1].value), p[0]) for p in props])
        return ((x.name, x.value) for x in cls)


class Sobre(ModelBase):
    sobre = RichTextField()

    logradouro = models.CharField("Logradouro", null=False, blank=False, max_length=150)
    numero = models.CharField("Número", null=False, blank=True, max_length=30)
    bairro = models.CharField("Bairro", null=False, blank=False, max_length=150)
    cidade = models.CharField("Cidade", null=False, blank=False, max_length=150)
    cep = models.CharField("CEP", null=False, blank=False, max_length=10)
    uf = models.CharField(max_length=2,
                          choices=Uf.choices(),
                          default=Uf.RJ.name,
                          null=False, blank=False)
    complemento = models.CharField("Complemento", null=False, blank=True, max_length=150)

    telefone = models.CharField(max_length=15, blank=True, null=True)
    telefone_2 = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)

    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    criado_por = models.ForeignKey(Usuario, related_name='sobre_criadas', default=1, on_delete=models.CASCADE)
    modificado_por = models.ForeignKey(Usuario, related_name='sobre_modificadas', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sobre[:30]

    class Meta:
        verbose_name = 'Dados Institucionais'
        verbose_name_plural = 'Dados Institucionais'