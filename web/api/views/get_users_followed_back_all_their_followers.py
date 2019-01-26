from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_users_followed_back_all_their_followers(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    if database.get_user_type_query(user_id) in ['admin', 'analyst']:
        users = database.get_users_followed_back_all_their_followers_query()
        return JsonResponse({'users': users}, status=200)
    else:
        return JsonResponse({'error': "permission denied"}, status=403)