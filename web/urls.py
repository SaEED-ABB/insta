from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('users/', views.user_list, name='user_list'),
    path('users/register/', views.register_user, name='register_user'),
    path('users/<int:user_id>/', views.user_home, name='user_home'),
    path('users/<int:user_id>/info/', views.user_info, name='user_info'),
    path('users/login/', views.login, name='login'),
    path('users/search/', views.search, name='search'),
    path('users/panel/', views.panel, name='panel'),
]
