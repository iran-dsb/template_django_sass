from contato.forms import ContatoModelForm
from contato.models import Mensagem
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages

class ContatoView(CreateView):
    model = Mensagem
    template_name = 'contato.html'
    form_class = ContatoModelForm
    success_url = reverse_lazy('contato:contato')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        args = self.get_form_kwargs()
        args.update({'request': self.request})
        return form_class(**args)

    def form_valid(self, form):
        messages.success(self.request, 'Mensagem enviada com sucesso.')
        return super().form_valid(form)



