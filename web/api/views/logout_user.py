from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def logout_user(request):
    if request.session.session_key in request.session:
        del request.session[request.session.session_key]

    return JsonResponse({'success': "successful logout"}, status=201)
