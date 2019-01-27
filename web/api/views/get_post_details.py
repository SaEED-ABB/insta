from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_post_details(request):
    post_id = request.GET['post_id']
    user_id = get_logged_in_user_id(request)

    result = database.get_post_details_query(post_id=post_id, user_id=user_id)
    return JsonResponse(result, status=200)
