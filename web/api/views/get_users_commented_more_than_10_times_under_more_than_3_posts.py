from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_users_commented_more_than_10_times_under_more_than_3_posts(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    if database.get_user_type_query(user_id) in ['admin']:
        users = database.get_users_commented_more_than_10_times_under_more_than_3_posts_query()
        return JsonResponse({'users': users}, status=200)
    else:
        return JsonResponse({'error': "permission denied"}, status=403)