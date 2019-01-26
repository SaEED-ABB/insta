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
    # query = """WITH followers AS (SELECT user_id FROM follows WHERE following_user_id = users.id),
    # followings AS (SELECT following_user_id FROM follows WHERE user_id = users.id)
    # SELECT * FROM users WHERE (followers) IN (followings);"""
    query = """SELECT * FROM users WHERE 
    (SELECT user_id FROM follows WHERE following_user_id = users.id) 
    IN 
    (SELECT following_user_id FROM follows WHERE user_id = users.id);"""

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [dict(zip(('id', 'email', 'username', 'password', 'type', 'question_id', 'answer', 'bio'), row)) for row in rows]
    return users


def get_users_whose_following_users_are_active_query():
    query = """SELECT * FROM users WHERE 
    users.id 
    IN 
    (SELECT following_user_id FROM follows WHERE 
        (follows.user_id = users.id) 
        AND 
        (follows.user_id IN 
            (SELECT user_id FROM posts WHERE posts.date > NOW() - INTERVAL '24 hour')
        )
    );"""

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [dict(zip(('id', 'email', 'username', 'password', 'type', 'question_id', 'answer', 'bio'), row)) for row in rows]
    return users


def get_last_posts_of_following_users_query(user_id):
    result = {}

    q1_posts = """SELECT posts.id, posts.date, posts.context, posts.user_id, users.username, 
    (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id), 
    (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id)
    FROM posts 
    INNER JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (SELECT follows.following_user_id FROM follows WHERE follows.user_id = %s)
    ORDER BY posts.date DESC LIMIT 100;""" % user_id

    q2_followings_count = """SELECT COUNT(*) FROM follows WHERE follows.user_id = %s;""" % user_id

    q3_followers_count = """SELECT COUNT(*) FROM follows WHERE follows.following_user_id = %s;""" % user_id

    q4_username = """SELECT username FROM users WHERE id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(q1_posts)
    rows = cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'user_id', 'user_username', 'likes_count', 'comments_count'), row)) for row in rows]
    result['posts'] = posts
    result['posts_count'] = len(posts)

    cursor.execute(q2_followings_count)
    row = cursor.fetchone()
    result['followings_count'] = row[0]

    cursor.execute(q3_followers_count)
    row = cursor.fetchone()
    result['followers_count'] = row[0]

    cursor.execute(q4_username)
    row = cursor.fetchone()
    result['username'] = row[0]
    result['user_id'] = user_id

    return result


def get_user_page_info_query(user_id):
    result = {}

    q1_posts = """SELECT posts.id, posts.date, posts.context, 
        (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id), 
        (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id)
        FROM posts 
        INNER JOIN users ON posts.user_id = users.id
        WHERE posts.user_id = %s
        ORDER BY posts.date DESC;""" % user_id

    q2_followings = """SELECT follows.following_user_id, users.username 
        FROM follows 
        INNER JOIN users ON users.id = follows.following_user_id
        WHERE follows.user_id = %s;""" % user_id

    q3_followers = """SELECT follows.user_id, users.username 
    FROM follows 
    INNER JOIN users ON users.id = follows.user_id
    WHERE follows.following_user_id = %s;""" % user_id

    q4_username = """SELECT username FROM users WHERE id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(q1_posts)
    rows = cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'likes_count', 'comments_count'), row)) for row in rows]
    result['posts'] = posts
    result['posts_count'] = len(posts)

    cursor.execute(q2_followings)
    rows = cursor.fetchall()
    followings = [dict(zip(('id', 'username'), row)) for row in rows]
    result['followings'] = followings
    result['followings_count'] = len(followings)

    cursor.execute(q3_followers)
    rows = cursor.fetchall()
    followers = [dict(zip(('id', 'username'), row)) for row in rows]
    result['followers'] = followers
    result['followers_count'] = len(followers)

    cursor.execute(q4_username)
    row = cursor.fetchone()
    result['username'] = row[0]
    result['user_id'] = user_id

    return result


def get_post_details_query(post_id):
    result = {}

    q1_post_detail = """SELECT posts.*, users.username 
    FROM posts 
    INNER JOIN users ON posts.user_id = users.id
    WHERE posts.id = %s;""" % post_id

    q2_post_likes = """SELECT posts_likes.user_id, users.username 
    FROM posts_likes 
    INNER JOIN users ON posts_likes.user_id = users.id
    WHERE posts_likes.post_id = %s;""" % post_id

    q3_post_comments = """SELECT comments.date, comments.user_id, comments.parent_id, users.username,
    (SELECT COUNT(*) FROM comments_likes WHERE comments.id = comments_likes.comment_id) 
    FROM comments 
    INNER JOIN users ON comments.user_id = users.id
    WHERE comments.post_id = %s;""" % post_id

    cursor = get_database_connection()
    cursor.execute(q1_post_detail)
    row = cursor.fetchone()
    result['post'] = dict(zip(('id', 'date', 'context', 'user_id', 'user_username'), row))

    cursor.execute(q2_post_likes)
    rows = cursor.fetchall()
    likes = [dict(zip(('liker_id', 'liker_username'), row)) for row in rows]
    result['post']['likes'] = likes
    result['post']['likes_count'] = len(likes)

    cursor.execute(q3_post_comments)
    rows = cursor.fetchall()
    comments = [dict(zip(('date', 'user_id', 'parent_id', 'user_username'), row)) for row in rows]
    result['post']['comments'] = comments
    result['post']['comments_count'] = len(comments)

    return result


def get_user_id_for_login_query(username, password):
    query = """SELECT id FROM users WHERE username = '%s' AND password = '%s';""" % (username, password)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def get_hottest_posts_query(order_by_date):
    query = """SELECT * FROM 
        (SELECT posts.id, posts.date, posts.context, posts.user_id, users.username, 
            (SELECT COUNT(posts_likes.*) FROM posts_likes WHERE posts.id = posts_likes.post_id) AS likes_count, 
            (SELECT COUNT(comments.*) FROM comments WHERE posts.id = comments.post_id) AS comments_count,
            (SELECT COUNT(comments_likes.*) 
                FROM comments_likes 
                INNER JOIN comments ON comments_likes.comment_id = comments.id
                WHERE posts.id = comments.post_id
            ) AS comments_likes_count
            FROM posts 
            INNER JOIN users ON posts.user_id = users.id) AS posts_info
        WHERE (likes_count + comments_count + comments_likes_count) > 0
        ORDER BY (likes_count + comments_count + comments_likes_count) {} DESC;""".format(",date" if order_by_date else "")

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'user_id', 'user_username', 'likes_count', 'comments_count', 'comments_likes_count'), row)) for row in rows]
    return posts
