from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def create_hash_tag(request):
    hash_tag = request.POST['hash_tag']
    post_id = request.POST['post_id']

    hash_tag_id = database.create_hash_tag_query(hash_tag=hash_tag, post_id=post_id)

    return JsonResponse({'id': hash_tag_id}, status=201)
