from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def like_post(request):
    post_id = request.POST['post_id']
    user_id = request.POST['user_id']

    like_id = database.like_post_query(post_id=post_id, user_id=user_id)

    return JsonResponse({'id': like_id}, status=201)
