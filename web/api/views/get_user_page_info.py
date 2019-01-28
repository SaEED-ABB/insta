from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def get_user_page_info(request):
    user_id = request.GET['user_id']
    logged_in_user_id = get_logged_in_user_id(request)

    result = database.get_user_page_info_query(user_id=user_id, logged_in_user_id=logged_in_user_id)
    return JsonResponse({'user_info': result}, status=200)
