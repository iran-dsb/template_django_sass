from django.db import models

from core.models.abstratas.Uf import Uf
from django.db.models import CASCADE, PROTECT


class EnderecoModel(models.Model):
    logradouro = models.CharField("Logradouro", null=True, blank=True, max_length=150)
    numero = models.CharField("Número", null=True, blank=True, max_length=30)
    bairro = models.CharField("Bairro", null=True, blank=True, max_length=150)
    municipio = models.ForeignKey('core.Municipio', null=True, blank=True, on_delete=PROTECT)
    cidade = models.CharField("Cidade", null=True, blank=True, max_length=150)
    cep = models.CharField("CEP", null=True, blank=True, max_length=10)
    uf = models.CharField(max_length=2,
                          choices=Uf.choices(),
                          default=Uf.RJ.name,
                          null=True, blank=True)
    complemento = models.CharField("Complemento", null=True, blank=True, max_length=150)

    class Meta:
        abstract = True