from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def like_post(request):
    post_id = request.POST['post_id']
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    like_id = database.like_post_query(post_id=post_id, user_id=user_id)

    return JsonResponse({'id': like_id}, status=201)
