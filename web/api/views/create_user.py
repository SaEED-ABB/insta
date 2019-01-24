from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def create_user(request):
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    type = request.POST['type']
    question_id = request.POST['question_id']
    answer = request.POST['answer']
    bio = request.POST.get('bio')

    user_id = database.create_user_query(email=email, username=username, password=password, type=type,
                               question_id=question_id, answer=answer, bio=bio)
    return JsonResponse({'id': user_id}, status=201)