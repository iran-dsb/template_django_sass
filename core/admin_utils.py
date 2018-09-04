from django.utils import timezone


def status_aprovado_update(change, form, obj, status_aprovacao):
    if change:
        # verifica se modificou status para aprovado
        if 'status' in form.changed_data and obj.status == status_aprovacao:
            obj.aprovado_em = timezone.now()
            obj.aprovado_por = form.user
        elif obj.status != status_aprovacao:
            obj.aprovado_em = None
            obj.aprovado_por = None
    else:
        # Verifica se status é aprovado
        if obj.status == status_aprovacao:
            obj.aprovado_em = timezone.now()
            obj.aprovado_por = form.user