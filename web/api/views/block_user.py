from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def block_user(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)
    blocked_user_id = request.POST['blocked_user_id']

    blocked_blockers_count, blocker_blockeds_count = database.block_user_query(user_id=user_id, blocked_user_id=blocked_user_id)

    return JsonResponse({'blocked_blockers_count': blocked_blockers_count,
                         'blocker_blockeds_count': blocker_blockeds_count}, status=201)

