import psycopg2
from insta.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def get_database_connection():
    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return cursor


def get_users_query():
    cursor = get_database_connection()
    cursor.execute("""SELECT * FROM users;""")
    rows = cursor.fetchall()
    return rows


def create_question_query(context):
    columns = "(context)"
    values = "('%s')" % context
    query = """INSERT INTO questions %s VALUES %s RETURNING id;""" % (columns, values)
    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_user_query(email, username, password, type, question_id=None, answer=None, bio=None):
    columns = "(email, username, password, type, question_id, answer, bio)"
    values = "('%s', '%s', '%s', %s, %s, '%s', '%s')" % (email, username, password, type, question_id, answer, bio)
    query = """INSERT INTO users %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_post_query(caption, user_id):
    columns = "(caption, user_id)"
    values = "('%s', %s)" % (caption, user_id)
    query = """INSERT INTO posts %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_comment_query(**kwargs):
    pass