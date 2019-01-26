from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def like_comment(request):
    comment_id = request.POST['comment_id']
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    comment_likes_count = database.like_comment_query(comment_id=comment_id, user_id=user_id)

    return JsonResponse({'comment_likes_count': comment_likes_count}, status=201)
