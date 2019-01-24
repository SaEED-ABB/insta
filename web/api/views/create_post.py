from django.http import JsonResponse
from insta.db import database
from django.views.decorators.http import require_POST


@require_POST
def create_post(request):
    context = request.POST['context']
    user_id = request.POST['user_id']

    words = context.split()
    hash_tag_words = []
    for word in words:
        hash_tag_words.extend(['#{}'.format(hash_tag_word) for hash_tag_word in word.split('#')[1:] if len(hash_tag_word) > 0])

    if len(hash_tag_words) >= 2:
        post_id = database.create_post_query(context=context, user_id=user_id)
        for hash_tag_word in hash_tag_words:
            database.create_hash_tag_query(hash_tag=hash_tag_word, post_id=post_id)
        return JsonResponse({'id': post_id}, status=201)
    else:
        return JsonResponse({'error': 'only posts with at least 2 hash tags allowed'})
