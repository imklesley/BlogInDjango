from django.urls import path
# API Views
from blog.api.views import (api_detail_blog_view, api_update_blog_view,
                            api_delete_blog_view, api_create_blog_view, ApiListView, api_list_view, api_user_posts)

app_name = 'blog_api'

urlpatterns = [

    path('<slug:slug>/', api_detail_blog_view, name='detail'),
    path('<slug:slug>/update', api_update_blog_view, name='update'),
    path('<slug:slug>/delete', api_delete_blog_view, name='delete'),
    path('create', api_create_blog_view, name='create'),
    path('my-posts', api_user_posts, name='user-posts'),
    path('list-by-classview', ApiListView.as_view(), name='list-by-classview'),
    path('list', api_list_view, name='list'),

]
