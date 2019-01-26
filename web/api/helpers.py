
def get_logged_in_user_id(request):
    if request.session.session_key in request.session:
        return request.session[request.session.session_key]
