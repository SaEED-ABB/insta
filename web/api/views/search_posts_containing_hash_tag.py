from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET
from ..helpers import get_logged_in_user_id


@require_GET
def search_posts_containing_hash_tag(request):
    # user_id = get_logged_in_user_id(request)
    # if not user_id:
    #     return JsonResponse({'error': "please login first"}, status=403)
    hash_tag = request.GET['hash_tag']
    user_id = request.GET['user_id']
    posts = database.search_posts_containing_hash_tag_query(hash_tag=hash_tag, logged_in_user_id=user_id)
    return JsonResponse({'posts': posts}, status=200)
