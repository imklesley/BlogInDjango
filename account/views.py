from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from blog.models import BlogPost

# Referencia-se o form criado
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


# Create your views here.


def registration_view(request):
    context = {}

    # se a requisição pela url foi do tipo POST
    if request.POST:
        # Mostro o form criado em from account.forms import RegistrationForm e coloco o retorno em "form"
        form = RegistrationForm(request.POST)
        if form.is_valid():  # Verifica-se se todos os campos estão válidos
            form.save()  # Caso estejam, salva-se o formulário

            # Pega-se os valores de cada campo do formulário
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            raw_password = form.cleaned_data.get('password1')

            # Realiza a criação do novo usuário no sistema
            account = authenticate(email=email, username=username, first_name=first_name, password=raw_password)
            # Após o usuário estiver logado basta logar na conta, caso assim deseje
            login(request=request, user=account)
            # Após isso se retorna/redireciona para alguma página, no caso redirecionamos para 'home'
            return redirect('home')
        else:
            # caso ocorra erros, salvo o formulário em "registration_form"
            context['registration_form'] = form
    else:
        # Se não é um POST é um GET, logo é a primeira vez que estão vendo o formulário, logo exibo para o usuário
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user

    # Usuário já está autenticado? se sim redireciona para home
    if user.is_authenticated:
        return redirect('home')

    # Se a requisição é do tipo POST, significa o usuário já possui o form e está tentando enviar
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        # Verifica-se o form foi preenchido corretamente
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # Autentica-se o usuário
            user = authenticate(username=username, password=password)

            # Caso o retorno seja diferente de None, significa que o usuário existe e foi autenticado
            if user:
                # Realiza-se o login no user autenticado
                login(request, user)
                # redireciona para home
                return redirect('home')


    # Caso não seja do tipo POST, é do tipo GET. E Então o usuário está acessando o form pela primeira vez
    # Logo preciso gerar o form pra ele vizualizar
    else:
        # Criação do form
        form = AccountAuthenticationForm()

    # coloco no context como form_login
    context['login_form'] = form

    # renderizo o template passando o formulário
    return render(request=request, template_name='account/login.html', context=context)


def account_view(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountUpdateForm(request.POST,
                                 instance=user)  # é passado o user, pois no form é preciso acessar a pk do usuário logado
        if form.is_valid():
            form.initial = {
                'first_name': request.POST['first_name'],
                'username': request.POST['username'],
                'email': request.POST['email']
            }

            # Commit dos dados no bd
            form.save()
            context['sucess_message'] = 'Seus dados foram atualizados com sucesso !'



    else:
        form = AccountUpdateForm(initial={
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name
        })

    context['account_form'] = form

    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts

    return render(request=request, template_name='account/account.html', context=context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
