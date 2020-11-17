from django.shortcuts import render, redirect, get_object_or_404

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm
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
