from django.contrib import admin
from django.urls import path,include
from blog import views
urlpatterns = [
    path('get_all_blog_list',views.get_all_blog_list,name='get_all_blog_list'),
    path('get_blog_detail/<int:blog_id>',views.get_blog_detail_by_id,name='get_blog_detail'),
    path('get_blog_list_by_type/<int:blog_type_id>',views.get_blog_list_by_type,name='get_blog_list_by_type'),
    path('get_blog_list_by_year_month/<int:year>/<int:month>',views.get_blog_list_by_year_month,name='get_blog_list_by_year_month')
]