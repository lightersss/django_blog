from django.urls import path,include
from . import views
urlpatterns = [
    path('submit_comment',views.submit_comment,name='submit_comment')
]