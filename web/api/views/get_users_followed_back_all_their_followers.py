from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def get_users_followed_back_all_their_followers(request):
    user_id = request.POST['user_id']
    if database.get_user_type_query(user_id) in ['admin', 'analyst']:
        users = database.get_users_followed_back_all_their_followers_query()
        return JsonResponse({'users': users}, status=200)
    else:
        return JsonResponse({'error': "permission denied"}, status=403)