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

    if not database.is_he_liking_his_own_comment(user_id=user_id, comment_id=comment_id):
        return JsonResponse({'error': "you can't like your own comment"}, status=400)

    if not database.is_he_liking_the_comment_of_his_blocker(user_id=user_id, comment_id=comment_id):
        return JsonResponse({'error': "you can't like the comment of your blocker"}, status=400)

    comment_likes_count = database.like_comment_query(comment_id=comment_id, user_id=user_id)

    return JsonResponse({'comment_likes_count': comment_likes_count}, status=201)
