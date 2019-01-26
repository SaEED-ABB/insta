from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_GET


@require_GET
def get_hottest_posts(request):
    order_by_date = request.GET.get('order_by_date')
    order_by_date = True if order_by_date == 'true' else False
    posts = database.get_hottest_posts_query(order_by_date=order_by_date)
    return JsonResponse({'posts': posts}, status=200)
