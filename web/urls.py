from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('api/questions/create/', views.create_question, name='create_question'),
    path('api/posts/create/', views.create_post, name='create_post'),
]
