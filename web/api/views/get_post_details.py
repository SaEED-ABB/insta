from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def get_post_details(request):
    post_id = request.GET['post_id']

    result = database.get_post_details_query(post_id=post_id)
    return JsonResponse(result, status=200)
