from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def create_comment(request):
    context = request.POST['context']
    parent_id = request.POST.get('parent_id')
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)
    post_id = request.POST['post_id']

    if parent_id and database.has_comment_depth_more_than_one(parent_id=parent_id):
        return JsonResponse({'error': "comments with depth more than one not allowed"}, status=400)

    comment_id = database.create_comment_query(context=context, parent_id=parent_id, user_id=user_id, post_id=post_id)

    return JsonResponse({'id': comment_id}, status=201)
