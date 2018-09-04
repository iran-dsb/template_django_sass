from django.db.models.query import QuerySet
from django.utils import timezone


class NoticiasQueryset(QuerySet):
    def publicadas(self, exclude_ids_list=None):
        from noticias.models import Noticia
        qs = self.filter(
            status=Noticia.APROVADA,
            data_publicacao__lte=timezone.localtime(timezone.now())
        ).select_related('categoria', 'criado_por').prefetch_related('tags', 'imagens').order_by('-data_publicacao')
        if exclude_ids_list:
            qs = qs.exclude(id__in=exclude_ids_list)
        return qs

    def publicadas_categoria(self, categoria, exclude_ids_list=None):
        qs = self.publicadas(exclude_ids_list).filter(categoria=categoria)
        return qs

    def get_destaque(self, local_destaque):
        noticia = self.publicadas().filter(
            destaque=local_destaque,
            data_destaque__lte=timezone.localtime(timezone.now())
        ).order_by('-data_destaque').first()
        return noticia

    def get_ultimas(self, exclude_ids_list=None):
        noticias = self.publicadas(exclude_ids_list).order_by('-data_publicacao')[:5]

        return noticias

    def get_destaque_quantidade(self, local_destaque, quantidade):
        noticia = self.publicadas().filter(
            destaque=local_destaque,
            data_destaque__lte=timezone.localtime(timezone.now())
        ).order_by('-data_destaque')[:quantidade]
        return noticia

    def get_all_destaques(self):
        from noticias.models import Noticia
        noticias = {}
        for local_destaque in Noticia.LOCAIS_DESTAQUE:
            noticias[local_destaque[0]] = self.get_destaque(local_destaque[0])
        return noticias

    def publicadas_tags(self, tags_list, exclude_ids_list=None):
        try:
            qs = self.publicadas(exclude_ids_list).filter(
                tags__in=tags_list
            )
        except:
            qs = self.publicadas(exclude_ids_list).filter(
                tags__slug__in=tags_list
            )
        return qs.distinct()

    def publicadas_categoria_tags(self, categoria, tags_list, exclude_ids_list=None):
        qs = self.publicadas_categoria(categoria, exclude_ids_list)
        try:
            qs = qs.filter(tags__in=tags_list)
        except:
            qs = qs.filter(tags__slug__in=tags_list)
        return qs.distinct()