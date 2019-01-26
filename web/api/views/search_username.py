from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def search_username(request):
    username = request.GET['username']

    users = database.search_username_query(username=username)
    return JsonResponse({'users': users}, status=200)
