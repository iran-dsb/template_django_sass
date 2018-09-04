from django.db.models.query import QuerySet
from django.utils import timezone


class GaleriasQueryset(QuerySet):
    def publicadas(self, exclude_ids_list=None):
        qs = self.filter(
            ativa=True,
            data_publicacao__lte=timezone.localtime(timezone.now())
        ).prefetch_related('imagens').order_by('-data_publicacao')
        if exclude_ids_list:
            qs = qs.exclude(id__in=exclude_ids_list)
        return qs


class FotoGaleriaQueryset(QuerySet):
    def get_fotos_pousada(self):
        qs = self.filter(
            galeria__ativa=True,
            galeria__data_publicacao__lte=timezone.localtime(timezone.now()),
            galeria__pousada=True
        )
        return qs

    def get_fotos(self):
        qs = self.filter(
            galeria__ativa=True,
            galeria__data_publicacao__lte=timezone.localtime(timezone.now()),
        )
        return qs