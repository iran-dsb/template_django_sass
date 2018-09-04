from contato.email import sendEmail
from contato.models import Mensagem
from django import forms


class ContatoModelForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ('nome', 'email', 'telefone', 'mensagem')
        widgets = {'mensagem': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = 'Seu Nome'
        self.fields['email'].label = 'Seu E-mail'
        self.fields['telefone'].label = 'Seu Telefone'
        self.fields['mensagem'].label = 'Sua Mensagem'
        if request:
            self.request = request

    def save(self, commit=True):
        self.instance.assunto = 'Contato site - {0} - {1}'.format(
            self.instance.nome,
            self.instance.email
        )
        try:
            sendEmail(self.instance, self.request)
        except Exception as ex:
            print(ex)
        finally:
            return super().save(commit)


