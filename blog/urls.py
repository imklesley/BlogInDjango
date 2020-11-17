# Dentro da seção blog -appblog terá seu próprio conjunto de urls

from django.urls import path
from blog.views import create_blog_view, detail_blog_view

# parâmetro obrigatório, quando se tem urls de um determinado app
app_name = 'blog'

urlpatterns = [

    path('create/', create_blog_view, name='create'),
    path('<slug>/', detail_blog_view, name='detail')

]
