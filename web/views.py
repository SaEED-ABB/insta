from django.shortcuts import render
from insta.db import database
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html', {})


def user_list(request):
    users = database.get_users_query()
    return render(request, 'user_list.html', {'users': users})


def create_user(request):
    if request.method == 'POST':
        import random
        id = str(random.randint(0, 1000))
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        type = request.POST['type']
        answer = request.POST['answer']

        database.create_user_query(id=id, email=email, username=username, password=password, type=type, answer=answer)
        return JsonResponse({})
    else:
        return render(request, 'create_user.html', {})
