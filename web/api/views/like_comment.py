from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def like_comment(request):
    comment_id = request.POST['comment_id']
    user_id = request.POST['user_id']

    comment_id = database.like_comment_query(comment_id=comment_id, user_id=user_id)

    return JsonResponse({'id': comment_id}, status=201)
