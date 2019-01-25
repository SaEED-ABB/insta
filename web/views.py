from django.shortcuts import render
from insta.db import database


def index(request):
    return render(request, 'index.html', {})


def user_list(request):
    users = database.get_users_query()
    return render(request, 'user_list.html', {'users': users})


def register_user(request):
    return render(request, 'register.html')


def create_post(request):
    return render(request, 'user.html')

def like_post(request):
    return render(request, 'user.html')