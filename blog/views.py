from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account


def create_blog_view(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    # vai ser um request do tipo POST ou nada
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        # o paramentro commit precisa está False, pois ainda falta setar o "author" do post
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form
    return render(request, 'blog/create_blog.html', context)


def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)

    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)


    if not blog_post.author == user:
        return HttpResponse('<p>Somente o dono da postagem pode realizar edições!!</p>')


    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Atualizado com sucesso!"
            blog_post = obj

    form = UpdateBlogPostForm(

        initial={
            'title': blog_post.title,
            'body': blog_post.body,
            'image': blog_post.image
        }

    )

    context['form'] = form

    return render(request, 'blog/edit_blog.html', context)



def get_blog_queryset(query=None):
    #Lista que vai receber os posts únicos encontrados
    queryset = []
    #separa as palavras da frase para buscar cada uma separada
    queries = query.split('  ')

    for q in queries:

        posts = BlogPost.objects.filter(
            Q(title__icontains=q),
            Q(body__icontains=q),
        ).distinct()
        #adiciona os posts encontrados em queryset
        for post in posts:
            queryset.append(post)
    #Remove-se os posts repetidos usando o set, transforma em lista e retorna
    return list(set(queryset))