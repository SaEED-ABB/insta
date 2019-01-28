from django.shortcuts import render
from insta.db import database


def index(request):
    return render(request, 'index.html', {})


def user_list(request):
    users = database.get_users_query()
    return render(request, 'user_list.html', {'users': users})


def register_user(request):
    return render(request, 'register.html')


def user_home(request, user_id):
    return render(request, 'user_home.html')


def user_info(request, user_id):
    return render(request, 'user_info.html')


def login(request):
    return render(request, 'login.html')

def search(request):
    return render(request, 'search.html')

def panel(request):
    return render(request, 'panel.html')