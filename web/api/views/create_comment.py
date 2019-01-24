from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def create_comment(request):
    context = request.POST['context']
    parent_id = request.POST.get('parent_id')
    user_id = request.POST['user_id']
    post_id = request.POST['post_id']

    comment_id = database.create_comment_query(context=context, parent_id=parent_id, user_id=user_id, post_id=post_id)

    return JsonResponse({'id': comment_id}, status=201)
