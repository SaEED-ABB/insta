from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user_list'),
    path('users/register/', views.register_user, name='register_user'),
    path('user/', views.create_post, name='create_post'),
    path('login/',views.login, name='login'),
    path('user_detail/', views.user_detail, name='user_detail'),
]
