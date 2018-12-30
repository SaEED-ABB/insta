from django.shortcuts import render
from insta.database import get_database_connection


def index(request):
    return render(request, 'index.html', {})


def user_list(request):
    conn = get_database_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM user;""")
    rows = cursor.fetchall()
    print(rows)
    return render(request, 'user_list.html', {'users': rows})
