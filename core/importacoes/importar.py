import xlrd
from core.models.enderecos import Regiao, Estado, Mesorregiao, Microrregiao, Municipio
from django.conf import settings
import os

from template_sass.settings import BASE_DIR

'''
1	Norte
2	Nordeste
3	Sudeste
4	Sul
5	Centro-Oeste


'''

Regioes = {
    1: 'Norte',
    2: 'Nordeste',
    3: 'Sudeste',
    4: 'Sul',
    5: 'Centro-Oeste',
}
estados = [
    (12, 1, 'AC', 'Acre'),
    (27, 2, 'AL', 'Alagoas'),
    (16, 1, 'AP', 'Amapá'),
    (13, 1, 'AM', 'Amazonas'),
    (29, 2, 'BA', 'Bahia'),
    (23, 2, 'CE', 'Ceará'),
    (53, 5, 'DF', 'Distrito Federal'),
    (32, 3, 'ES', 'Espírito Santo'),
    (52, 5, 'GO', 'Goiás'),
    (21, 2, 'MA', 'Maranhão'),
    (51, 5, 'MT', 'Mato Grosso'),
    (50, 5, 'MS', 'Mato Grosso do Sul'),
    (31, 3, 'MG', 'Minas Gerais'),
    (41, 4, 'PR', 'Paraná'),
    (25, 2, 'PB', 'Paraíba'),
    (15, 1, 'PA', 'Pará'),
    (26, 2, 'PE', 'Pernambuco'),
    (22, 2, 'PI', 'Piauí'),
    (33, 3, 'RJ', 'Rio de Janeiro'),
    (24, 2, 'RN', 'Rio Grande do Norte'),
    (43, 4, 'RS', 'Rio Grande do Sul'),
    (11, 1, 'RO', 'Rondônia'),
    (14, 1, 'RR', 'Roraima'),
    (42, 4, 'SC', 'Santa Catarina'),
    (28, 2, 'SE', 'Sergipe'),
    (35, 3, 'SP', 'São Paulo'),
    (17, 1, 'TO', 'Tocantins'),
]

# estados = {
#     1: [13, 14, 16, 15, 17, 11, 12],
#     2: [21, 22, 23, 24, 26, 25, 28, 27, 29],
#     5: [51, 50, 52, 53],
#     3: [35, 33, 32, 31],
#     4: [41, 43, 42],
# }
def migrar_regiao():
    regioes_list = []
    for k,v in Regioes.items():
        regioes_list.append(Regiao(id=k, descricao=v))
    print(regioes_list)
    return regioes_list
    #Regiao.objects.bulk_create(regioes_list)

def migrar_uf():
    estados_list = []
    for i in estados:
        estados_list.append(Estado(id=i[0], codigo=i[0], descricao=i[3],
                            sigla=i[2], regiao_id=i[1]))
    print(estados_list)
    #Estado.objects.bulk_create(estados_list)
    return estados_list


def migrar_mesoregiao():
    #DTB_BRASIL_MUNICIPIO.xls
    book = xlrd.open_workbook(os.path.join(BASE_DIR,'core', 'importacoes',"DTB_BRASIL_MUNICIPIO.xls"))
    sh = book.sheet_by_index(0)
    print(sh.name, sh.nrows, sh.ncols)
    meso_list = []
    for rx in range(1, sh.nrows):
        meso_list.append((sh.cell_value(rowx=rx, colx=0),
                          sh.cell_value(rowx=rx, colx=2),
                          sh.cell_value(rowx=rx, colx=3)))
        #print(sh.row(rx))
    meso_list_obj = []
    for i in meso_list:
        meso_list_obj.append(Mesorregiao(id=int(i[0] + i[1]), codigo=i[1], descricao=i[2],
                                   estado_id=int(i[0])))
    meso_list_obj = (list(set(meso_list_obj)))
    for o in meso_list_obj:
        print(o.codigo, o.descricao, o.estado_id)

    #Mesorregiao.objects.bulk_create(meso_list_obj)
    return meso_list_obj


def migrar_microregiao():
    #DTB_BRASIL_MUNICIPIO.xls
    book = xlrd.open_workbook(os.path.join(BASE_DIR,'core', 'importacoes',"DTB_BRASIL_MUNICIPIO.xls"))
    sh = book.sheet_by_index(0)
    print(sh.name, sh.nrows, sh.ncols)
    meso_list = []
    for rx in range(1, sh.nrows):
        meso_list.append((sh.cell_value(rowx=rx, colx=0),
                          sh.cell_value(rowx=rx, colx=2),
                          sh.cell_value(rowx=rx, colx=4),
                          sh.cell_value(rowx=rx, colx=5),
                          ))
        #print(sh.row(rx))
    micro_list_obj = []
    for i in meso_list:
        micro_list_obj.append(Microrregiao(id=int(i[0]+i[1]+i[2]), codigo=i[2], descricao=i[3],
                                          mesorregiao_id=int(i[0]+i[1])))
    micro_list_obj = (list(set(micro_list_obj)))
    for o in micro_list_obj:
        print(o.codigo, o.descricao, o.mesorregiao_id)
    print(len(micro_list_obj))
    #Microrregiao.objects.bulk_create(micro_list_obj)
    return micro_list_obj


def migrar_municipios():
    #DTB_BRASIL_MUNICIPIO.xls
    book = xlrd.open_workbook(os.path.join(BASE_DIR,'core', 'importacoes',"DTB_BRASIL_MUNICIPIO.xls"))
    sh = book.sheet_by_index(0)
    print(sh.name, sh.nrows, sh.ncols)
    meso_list = []
    for rx in range(1, sh.nrows):
        meso_list.append((sh.cell_value(rowx=rx, colx=0),
                          sh.cell_value(rowx=rx, colx=2),
                          sh.cell_value(rowx=rx, colx=4),
                          sh.cell_value(rowx=rx, colx=6),
                          sh.cell_value(rowx=rx, colx=7),
                          sh.cell_value(rowx=rx, colx=8),
                          ))
        #print(sh.row(rx))
    municipios = []
    for i in meso_list:
        municipios.append(Municipio(id=int(i[4]), codigo=i[3], codigo_completo=i[4], descricao=i[5],
                                    microrregiao_id=int(i[0]+i[1]+i[2])))
    municipios_list_obj = (list(set(municipios)))
    for o in municipios_list_obj:
        print(o.codigo, o.codigo_completo, o.descricao, o.microrregiao_id)
    print(len(municipios_list_obj))
    #Municipio.objects.bulk_create(municipios_list_obj)
    return municipios_list_obj


def migrar_tudo():
    migrar_regiao()
    migrar_uf()
    migrar_mesoregiao()
    migrar_microregiao()
    migrar_municipios()