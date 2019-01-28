from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_question_for_logged_in_user(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    question = database.get_question_for_logged_in_user_query(user_id=user_id)
    return JsonResponse({'question': question}, status=200)
