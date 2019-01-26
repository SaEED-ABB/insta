from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def follow_user(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)
    following_user_id = request.POST['following_user_id']

    follow_id = database.follow_user_query(user_id=user_id, following_user_id=following_user_id)

    return JsonResponse({'id': follow_id}, status=201)
