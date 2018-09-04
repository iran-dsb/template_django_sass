from enum import Enum, unique


import inspect

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
