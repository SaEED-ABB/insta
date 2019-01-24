from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def block_user(request):
    user_id = request.POST['user_id']
    blocked_user_id = request.POST['blocked_user_id']

    block_id = database.block_user_query(user_id=user_id, blocked_user_id=blocked_user_id)

    return JsonResponse({'id': block_id}, status=201)

