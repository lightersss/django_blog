from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.user_regsier, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('login_from_modal', views.login_from_modal, name='login_from_modal'),
    path('get_user_info', views.get_user_info, name='get_user_info'),
    path('change_email', views.change_email, name='change_email'),
    path('send_email_verify_code', views.send_email_verify_code, name='send_email_verify_code'),
]
