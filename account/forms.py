from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        # Aviso o django qual deve ser a estrutura do form, isso baseando-se no modelo criado anteriormente
        # Aqui é explicado quais valores são requeridos, unicos e etc
        model = Account
        fields = ('first_name', 'email', 'username', 'password1', 'password2')

    # Pode se usar a função clean e limpar todas var ou pode-se realiza separadamente:

    def clean_first_name(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field username
            first_name = self.cleaned_data['first_name']
            return first_name

    def clean_username(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field username
            username = self.cleaned_data['username']
            try:
                # tenta encontrar algum conta que já utiliza aquele username
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:  # Caso não encontre retornar o username
                return username
            else:
                # Caso encontre, mostra uma mensagem de error
                raise forms.ValidationError(f'Username "{username}" já está em uso.')

    def clean_email(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field email
            email = self.cleaned_data['email']
            try:
                # tenta encontrar algum conta que já utiliza aquele email
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:  # Caso não encontre retornar o email
                return email
            # Caso encontre, mostra uma mensagem de error
            raise forms.ValidationError(f'Email "{email}" já está em uso.')


class AccountAuthenticationForm(forms.ModelForm):
    # Digo qual a o nome quero dentro do campo de senha, e digo que o campo é do tipo senha logo ele obcuresse o texto
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    username = forms.CharField(label='Username', )

    class Meta:
        # Falo pro django quais são as cofigurações do form
        model = Account
        fields = ('username', 'password')

    def clean(self):
        # se o formulário for válido, logo posso coletar o username e senha informados pelo usuário
        if self.is_valid():
            # antes de rodar qualquer coisa é executado esse método para coletar os dados
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            # Non Field Error, caso o campo não esteja preenchido aparecer esse error
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Credenciais Inválidas!', code='invalid')


class AccountUpdateForm(forms.ModelForm):

    username = forms.CharField(label='Username')

    class Meta:
        model = Account
        fields = ('first_name', 'username', 'email',)

    # Pode se usar a função clean e limpar todas var ou pode-se realiza separadamente:

    def clean_first_name(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field username
            first_name = self.cleaned_data['first_name']
            return first_name

    def clean_username(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field username
            username = self.cleaned_data['username']
            try:
                # tenta encontrar algum conta que já utiliza aquele username
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:  # Caso não encontre retornar o username
                return username
            else:
                # Caso encontre, mostra uma mensagem de error
                raise forms.ValidationError(f'Username "{username}" já está em uso.')

    def clean_email(self):
        # verifica-se validade do form
        if self.is_valid():
            # pega-se os dados do field email
            email = self.cleaned_data['email']
            try:
                # tenta encontrar algum conta que já utiliza aquele email
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:  # Caso não encontre retornar o email
                return email
            # Caso encontre, mostra uma mensagem de error
            raise forms.ValidationError(f'Email "{email}" já está em uso.')












