from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_last_posts_of_following_users(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    posts = database.get_last_posts_of_following_users_query(user_id=user_id)
    return JsonResponse({'posts': posts}, status=200)