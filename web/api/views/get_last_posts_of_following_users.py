from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def get_last_posts_of_following_users(request):
    user_id = request.GET['user_id']

    posts = database.get_last_posts_of_following_users_query(user_id=user_id)
    return JsonResponse({'posts': posts}, status=200)