from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def get_users_whose_following_users_are_active(request):
    user_id = request.GET['user_id']
    if database.get_user_type_query(user_id) in ['admin', 'analyst']:
        users = database.get_users_whose_following_users_are_active_query()
        return JsonResponse({'users': users}, status=200)
    else:
        return JsonResponse({'error': "permission denied"}, status=403)