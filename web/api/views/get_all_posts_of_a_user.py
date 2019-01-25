from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def get_all_posts_of_a_user(request):
    user_id = request.GET['user_id']

    posts = database.get_all_posts_of_a_user_query(user_id=user_id)
    return JsonResponse({'posts': posts}, status=200)