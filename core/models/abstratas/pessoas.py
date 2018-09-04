from django.db import models


class PessoaModel(models.Model):
    MASCULINO = 0
    FEMININO = 1
    SEXO = [
        (MASCULINO, 'Masculino'),
        (FEMININO, 'Feminino')
    ]

    nome = models.CharField('Nome', max_length=100, null=False, blank=False)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    cpf = models.CharField('CPF', max_length=15, null=True, blank=True)

    rg = models.CharField('RG', max_length=50, null=True, blank=True)
    data_emissao = models.DateField('Emissão', null=True, blank=True)
    orgao_emissor = models.CharField('Órgão', max_length=30, null=True, blank=True)


    titulo = models.CharField(max_length=20, verbose_name='Título',
                            blank=True, null=True)
    zona = models.CharField(max_length=20, verbose_name='Zona',
                            blank=True, null=True)
    secao = models.CharField(max_length=20, verbose_name='Seção',
                            blank=True, null=True)

    sexo = models.PositiveSmallIntegerField('Sexo', choices=SEXO, null=True, blank=True)
    nacionalidade = models.CharField('Nacionalidade', max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
