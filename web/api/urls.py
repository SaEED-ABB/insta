from django.urls import path
from . import views


urlpatterns = [
    path('users/create/', views.create_user, name='create_user'),
    path('questions/create/', views.create_question, name='create_question'),
    path('posts/create/', views.create_post, name='create_post'),
    path('comments/create/', views.create_comment, name='create_comment'),
    path('posts/like/', views.like_post, name='like_post'),
    path('comments/like/', views.like_comment, name='like_comment'),
    path('users/follow/', views.follow_user, name='follow_user'),
    path('users/block/', views.block_user, name='block_user'),
    path('hash_tags/create/', views.create_hash_tag, name='create_hash_tag'),
    path('users/followed_back_all_their_followers/', views.get_users_followed_back_all_their_followers, name='get_users_followed_back_all_their_followers'),
    path('users/whose_following_users_are_active/', views.get_users_whose_following_users_are_active, name='get_users_whose_following_users_are_active'),
    path('users/last_posts_of_following_users/', views.get_last_posts_of_following_users, name='get_last_posts_of_following_users'),
    path('users/user_page_info/', views.get_user_page_info, name='get_user_page_info'),
    path('users/post_details/', views.get_post_details, name='get_post_details'),
    path('users/login/', views.login_user, name='login_user'),
    path('users/logout/', views.logout_user, name='logout_user'),

]