from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.conf import settings


def sendEmail(contato, request):
    request_url = request.build_absolute_uri(
        reverse('home')
    )

    msg_text = render_to_string(
        'emails/contato.txt', {'contato': contato}
    )
    msg_html = render_to_string(
        'emails/contato.html', {
            'contato': contato, 'request_url': request_url}
    )

    mail = EmailMultiAlternatives(
        contato.assunto or 'Contato Site',
        msg_text,
        settings.DEFAULT_FROM_EMAIL,
        settings.EMAILS_CONTATO,
        reply_to=['{0} <{1}>'.format(contato.nome, contato.email)]
    )

    mail.attach_alternative(msg_html, 'text/html')

    mail.send()