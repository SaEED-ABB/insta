from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_forgotten_user_password(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    answer = request.GET['answer']
    if database.is_his_answer_correct_query(user_id=user_id, answer=answer):
        password = database.get_forgotten_user_password_query(user_id=user_id)
        return JsonResponse({'password': password}, status=200)
    else:
        return JsonResponse({'error': "your answer does not match"}, status=400)
