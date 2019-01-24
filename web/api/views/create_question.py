from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def create_question(request):
    context = request.POST['context']
    question_id = database.create_question_query(context=context)
    return JsonResponse({'id': question_id}, status=201)