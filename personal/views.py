from django.shortcuts import render
from operator import attrgetter
# from personal.models import Question
# from account.models import Account
from blog.models import BlogPost
from blog.views import get_blog_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator # os dois primeiros são tipos de erros


BLOG_POST_PER_PAGE = 10
def home_screen_view(request):
    # # Estou realizando um select * from TabelaQuestions
    # questions = Question.objects.all()
    # context = {'blog_name': 'Blog In Django', 'list_of_techs': ['Python', 'Django', 'Dart', 'Flutter'],
    #            'questions': questions}
    # print(request.headers)

    # Busco todas as linhas da Tabela Accounts
    # accounts = Account.objects.all()
    # context['accounts'] = accounts

    context = {}
    query = ''

    if request.GET:
        # Pega o valor de q, caso seja nada insira ''
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_published'), reverse=True)

    # Pagination
    ## pega o valor de "page", caso seja vazio insere 1
    page = request.GET.get('page', 1)
    #passo todos blogs e a quantidade que representa uma página(rola uma espécie de divisão)
    blog_posts_paginator =  Paginator(blog_posts,BLOG_POST_PER_PAGE)

    try:
        blog_posts =  blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts

    return render(request=request, template_name='personal/home.html', context=context)
