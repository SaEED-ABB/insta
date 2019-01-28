from django.http import JsonResponse
from django.views.decorators.http import require_GET
from insta.db.database import get_user_type_query


@require_GET
def get_logged_in_user_id(request):
    user_id = None
    user_type = None
    if request.session.session_key in request.session:
        user_id = request.session[request.session.session_key]
        user_type = get_user_type_query(user_id=user_id)
    return JsonResponse({'id': user_id, 'user_type': user_type}, status=200)
