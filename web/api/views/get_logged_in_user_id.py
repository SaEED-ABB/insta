from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_logged_in_user_id(request):
    user_id = None
    if request.session.session_key in request.session:
        user_id = request.session[request.session.session_key]
    return JsonResponse({'id': user_id}, status=200)
