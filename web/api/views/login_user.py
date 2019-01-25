from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def login_user(request):
    if not request.session.session_key:
        request.session.create()

    try:
        username = request.POST['username']
        password = request.POST['password']
        user_id = database.get_user_id_for_login_query(username=username, password=password)
        request.session[request.session.session_key] = user_id
        return JsonResponse({'id': user_id}, status=201)
    except TypeError:
        return JsonResponse({'error': "incorrect username or password given"}, status=400)
