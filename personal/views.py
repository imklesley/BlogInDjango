from django.shortcuts import render
# from personal.models import Question
from account.models import Account

# Create your views here.


def home_screen_view(request):
    # # Estou realizando um select * from TabelaQuestions
    # questions = Question.objects.all()
    # context = {'blog_name': 'Blog In Django', 'list_of_techs': ['Python', 'Django', 'Dart', 'Flutter'],
    #            'questions': questions}
    # print(request.headers)

    context = {}

    #Busco todas as linhas da Tabela Accounts
    accounts = Account.objects.all()

    context['accounts'] = accounts


    return render(request=request, template_name='personal/home.html', context=context)
