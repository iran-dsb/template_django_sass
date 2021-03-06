# Generated by Django 2.0.4 on 2018-05-23 20:49
from core.importacoes.importar import *
from django.db import migrations

def rodar_migrations(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    db_alias = schema_editor.connection.alias

    Regiao = apps.get_model("core", "Regiao")
    Estado = apps.get_model("core", "Estado")
    Mesorregiao = apps.get_model("core", "Mesorregiao")
    Microrregiao = apps.get_model("core", "Microrregiao")
    Municipio = apps.get_model("core", "Municipio")

    regioes_list = migrar_regiao()
    estados_list = migrar_uf()
    meso_list_obj = migrar_mesoregiao()
    micro_list_obj = migrar_microregiao()
    municipios_list_obj = migrar_municipios()

    Regiao.objects.using(db_alias).bulk_create(regioes_list)
    Estado.objects.using(db_alias).bulk_create(estados_list)
    Mesorregiao.objects.using(db_alias).bulk_create(meso_list_obj)
    Microrregiao.objects.using(db_alias).bulk_create(micro_list_obj)
    Municipio.objects.using(db_alias).bulk_create(municipios_list_obj)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180523_1618'),
    ]

    operations = [
        migrations.RunPython(rodar_migrations),
    ]
