from django.shortcuts import render
from insta.db import database
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html', {})


def user_list(request):
    users = database.get_users_query()
    return render(request, 'user_list.html', {'users': users})


def create_question(request):
    if request.method == 'POST':
        context = request.POST['context']
        question_id = database.create_question_query(context=context)
        return JsonResponse({'id': question_id}, status=201)


def create_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        type = request.POST['type']

        question_id = request.POST['question_id']
        answer = request.POST['answer']
        bio = request.POST['bio']

        user_id = database.create_user_query(email=email, username=username, password=password, type=type,
                                   question_id=question_id, answer=answer, bio=bio)
        return JsonResponse({'id': user_id}, status=201)
    else:
        return render(request, 'create_user.html', {})


def create_post(request):
    if request.method == 'POST':
        caption = request.POST['caption']
        # date = request.POST['date']
        user_id = request.POST['user_id']

        post_id = database.create_post_query(caption=caption, user_id=user_id)

        return JsonResponse({'id': post_id}, status=201)
