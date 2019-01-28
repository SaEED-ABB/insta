from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST
from ..helpers import get_logged_in_user_id


@require_POST
def change_user_password(request):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return JsonResponse({'error': "please login first"}, status=403)

    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    if database.does_his_old_password_match_query(user_id=user_id, old_password=old_password):
        database.change_user_password_query(user_id=user_id, new_password=new_password)
        return JsonResponse({'success': "your password changed successfully"}, status=201)
    else:
        return JsonResponse({'error': "your given password does not match"}, status=400)
