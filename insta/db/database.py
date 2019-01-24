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


def create_user_query(email, username, password, type, question_id, answer, bio):
    if bio:
        columns = "(email, username, password, type, question_id, answer, bio)"
        values = "('%s', '%s', '%s', '%s', %s, '%s', '%s')" % (email, username, password, type, question_id, answer, bio)
    else:
        columns = "(email, username, password, type, question_id, answer)"
        values = "('%s', '%s', '%s', '%s', %s, '%s')" % (email, username, password, type, question_id, answer)

    query = """INSERT INTO users %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_post_query(context, user_id):
    columns = "(context, user_id)"
    values = "('%s', %s)" % (context, user_id)
    query = """INSERT INTO posts %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_comment_query(context, parent_id, user_id, post_id):
    if parent_id:
        columns = "(context, parent_id, user_id, post_id)"
        values = "('%s', %s, %s, %s)" % (context, parent_id, user_id, post_id)
    else:
        columns = "(context, user_id, post_id)"
        values = "('%s', %s, %s)" % (context, user_id, post_id)
    query = """INSERT INTO comments %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def like_post_query(post_id, user_id):
    columns = "(post_id, user_id)"
    values = "(%s, %s)" % (post_id, user_id)
    query = """INSERT INTO posts_likes %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def like_comment_query(comment_id, user_id):
    columns = "(comment_id, user_id)"
    values = "(%s, %s)" % (comment_id, user_id)
    query = """INSERT INTO comments_likes %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def follow_user_query(user_id, following_user_id):
    columns = "(user_id, following_user_id)"
    values = "(%s, %s)" % (user_id, following_user_id)
    query = """INSERT INTO follows %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def block_user_query(user_id, blocked_user_id):
    columns = "(user_id, blocked_user_id)"
    values = "(%s, %s)" % (user_id, blocked_user_id)
    query = """INSERT INTO blocks %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def create_hash_tag_query(hash_tag, post_id):
    columns = "(hash_tag, post_id)"
    values = "('%s', %s)" % (hash_tag, post_id)
    query = """INSERT INTO hash_tags %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def get_user_type_query(user_id):
    query = """SELECT type FROM users WHERE id = %s""" % user_id

    cursor = get_database_connection()
    cursor.execute(query)
    type = cursor.fetchone()
    return type[0]


def get_users_followed_back_all_their_followers_query():
    query = """SELECT * FROM users WHERE ((SELECT user_id FROM follows WHERE following_user_id = users.id) in (SELECT following_user_id FROM follows WHERE user_id = users.id));"""

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def get_last_posts_of_following_users_query(user_id):
    following_users = """SELECT following_user_id FROM follows WHERE user_id = %s""" % user_id
    query = """SELECT * FROM users WHERE """