from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import api_register_user_view, api_login_account_view,api_user_data, api_update_user

app_name = 'account_api'

urlpatterns = [
    path('register', api_register_user_view, name='register_api'),
    path('login-authtoken', obtain_auth_token, name='login_api_authtoken'),
    path('login', api_login_account_view, name='login_api'),
    path('my_account', api_user_data, name='my_account'),
    path('update_account', api_update_user, name='update_account'),
]
