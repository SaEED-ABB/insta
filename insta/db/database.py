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


def create_post_query(context, user_id, hash_tags_count):
    columns = "(context, user_id, hash_tags_count)"
    values = "('%s', %s, %s)" % (context, user_id, hash_tags_count)
    query = """INSERT INTO posts %s VALUES %s RETURNING id;""" % (columns, values)

    cursor = get_database_connection()
    cursor.execute(query)
    id = cursor.fetchone()
    return id[0]


def has_comment_depth_more_than_one(parent_id):
    query = """SELECT parent_id FROM comments WHERE id IN (SELECT parent_id FROM comments WHERE id = %s);""" % parent_id
    cursor = get_database_connection()
    cursor.execute(query)
    grand_parent = cursor.fetchone()
    return True if grand_parent else False


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
    cursor = get_database_connection()
    try:
        columns = "(post_id, user_id)"
        values = "(%s, %s)" % (post_id, user_id)
        q_do_like = """INSERT INTO posts_likes %s VALUES %s;""" % (columns, values)
        cursor.execute(q_do_like)
    except:
        q_do_unlike = """DELETE FROM posts_likes WHERE post_id = %s AND user_id = %s;""" % (post_id, user_id)
        cursor.execute(q_do_unlike)

    q_post_likes_count = """SELECT COUNT(*) FROM posts_likes WHERE post_id = %s;""" % post_id
    cursor.execute(q_post_likes_count)
    post_likes_count = cursor.fetchone()

    return post_likes_count[0]


def is_he_liking_his_own_comment(user_id, comment_id):
    print(user_id, comment_id)
    query = """SELECT COUNT(*) FROM comments WHERE id = %s AND user_id = %s;""" % (comment_id, user_id)
    cursor = get_database_connection()
    cursor.execute(query)
    row = cursor.fetchone()
    print(row)
    return True if row[0] == 1 else False


def is_he_liking_the_comment_of_his_blocker_or_inversely(user_id, comment_id):
    query = """SELECT COUNT(*) FROM comments WHERE comments.id = %s 
    AND (
        (comments.user_id IN (SELECT blocks.user_id FROM blocks WHERE blocks.blocked_user_id = %s))
        OR
        (%s IN (SELECT blocks.user_id FROM blocks WHERE blocks.blocked_user_id = comments.user_id))
    );""" % (comment_id, user_id, user_id)
    cursor = get_database_connection()
    cursor.execute(query)
    row = cursor.fetchone()
    return True if row[0] == 1 else False


def like_comment_query(comment_id, user_id):
    cursor = get_database_connection()
    try:
        columns = "(comment_id, user_id)"
        values = "(%s, %s)" % (comment_id, user_id)
        q_do_like = """INSERT INTO comments_likes %s VALUES %s;""" % (columns, values)
        cursor.execute(q_do_like)
    except:
        q_do_unlike = """DELETE FROM comments_likes WHERE comment_id = %s AND user_id = %s;""" % (comment_id, user_id)
        cursor.execute(q_do_unlike)

    q_comment_likes_count = """SELECT COUNT(*) FROM comments_likes WHERE comment_id = %s;""" % comment_id
    cursor.execute(q_comment_likes_count)
    comment_likes_count = cursor.fetchone()

    return comment_likes_count[0]


def follow_user_query(user_id, following_user_id):
    cursor = get_database_connection()
    try:
        columns = "(user_id, following_user_id)"
        values = "(%s, %s)" % (user_id, following_user_id)
        q_do_follow = """INSERT INTO follows %s VALUES %s;""" % (columns, values)
        cursor.execute(q_do_follow)
    except:
        q_do_unfollow = """DELETE FROM follows WHERE user_id = %s AND following_user_id = %s;""" % (user_id, following_user_id)
        cursor.execute(q_do_unfollow)

    q_follower_followings_count = """SELECT COUNT(*) FROM follows WHERE user_id = %s;""" % user_id
    cursor.execute(q_follower_followings_count)
    follower_followings_count = cursor.fetchone()

    q_following_followers_count = """SELECT COUNT(*) FROM follows WHERE following_user_id = %s;""" % following_user_id
    cursor.execute(q_following_followers_count)
    following_followers_count = cursor.fetchone()

    return following_followers_count[0], follower_followings_count[0]


def block_user_query(user_id, blocked_user_id):
    cursor = get_database_connection()
    try:
        columns = "(user_id, blocked_user_id)"
        values = "(%s, %s)" % (user_id, blocked_user_id)
        q_do_block = """INSERT INTO blocks %s VALUES %s;""" % (columns, values)
        cursor.execute(q_do_block)
    except:
        q_do_unblock = """DELETE FROM blocks WHERE user_id = %s AND blocked_user_id = %s;""" % (user_id, blocked_user_id)
        cursor.execute(q_do_unblock)

    q_blocker_blocked_count = """SELECT COUNT(*) FROM blocks WHERE user_id = %s;""" % user_id
    cursor.execute(q_blocker_blocked_count)
    blocker_blockeds_count = cursor.fetchone()

    q_blocked_blockers_count = """SELECT COUNT(*) FROM blocks WHERE blocked_user_id = %s;""" % blocked_user_id
    cursor.execute(q_blocked_blockers_count)
    blocked_blockers_count = cursor.fetchone()

    return blocked_blockers_count[0], blocker_blockeds_count[0]


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
    query = """SELECT users.id, users.username FROM users WHERE 
    (SELECT COUNT(user_id) FROM follows WHERE 
        following_user_id = users.id
        AND 
        follows.user_id IN (SELECT following_user_id FROM follows WHERE user_id = users.id)
    ) 
    = 
    (SELECT COUNT(user_id) FROM follows WHERE following_user_id = users.id);"""

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [dict(zip(('id', 'username'), row)) for row in rows]
    return users


def get_users_whose_following_users_are_active_query():
    query = """SELECT users.id, users.username FROM users WHERE 
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
    users = [dict(zip(('id', 'username'), row)) for row in rows]
    return users


def get_last_posts_of_following_users_query(user_id):
    result = {}

    q1_posts = """SELECT posts.id, posts.date, posts.context, posts.user_id, users.username, 
    (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id), 
    (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id),
    (SELECT COUNT(*) FROM posts_likes WHERE posts_likes.post_id = posts.id AND posts_likes.user_id = %s)
    FROM posts 
    INNER JOIN users ON posts.user_id = users.id
    WHERE posts.user_id IN (SELECT follows.following_user_id FROM follows WHERE follows.user_id = %s)
    ORDER BY posts.date DESC LIMIT 100;""" % (user_id, user_id)

    q2_followings_count = """SELECT COUNT(*) FROM follows WHERE follows.user_id = %s;""" % user_id

    q3_followers_count = """SELECT COUNT(*) FROM follows WHERE follows.following_user_id = %s;""" % user_id

    q4_username = """SELECT username FROM users WHERE id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(q1_posts)
    rows = cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'user_id', 'user_username', 'likes_count', 'comments_count', 'has_current_user_liked'), row)) for row in rows]
    for i in range(len(posts)):
        posts[i]['hash_tags'] = get_post_hash_tags_query(post_id=posts[i]['id'])
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


def get_user_page_info_query(user_id, logged_in_user_id):
    result = {}

    q1_posts = """SELECT posts.id, posts.date, posts.context, 
        (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id), 
        (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id)
        FROM posts 
        INNER JOIN users ON posts.user_id = users.id
        WHERE posts.user_id = %s
        ORDER BY posts.date DESC;""" % user_id

    q2_followings = """SELECT follows.following_user_id, users.username,
        (SELECT COUNT(*) FROM follows WHERE user_id = %s AND following_user_id = users.id) AS you_followed_him,
        (SELECT COUNT(*) FROM blocks WHERE user_id = %s AND blocked_user_id = users.id) AS you_blocked_him
        FROM follows 
        INNER JOIN users ON users.id = follows.following_user_id
        WHERE follows.user_id = %s;""" % (logged_in_user_id, logged_in_user_id, user_id)

    q3_followers = """SELECT follows.user_id, users.username,
        (SELECT COUNT(*) FROM follows WHERE user_id = %s AND following_user_id = users.id) AS you_followed_him,
        (SELECT COUNT(*) FROM blocks WHERE user_id = %s AND blocked_user_id = users.id) AS you_blocked_him
        FROM follows 
        INNER JOIN users ON users.id = follows.user_id
        WHERE follows.following_user_id = %s;""" % (logged_in_user_id, logged_in_user_id, user_id)

    q4_username_and_bio = """SELECT username, bio FROM users WHERE id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(q1_posts)
    rows = cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'likes_count', 'comments_count'), row)) for row in rows]
    for i in range(len(posts)):
        posts[i]['hash_tags'] = get_post_hash_tags_query(post_id=posts[i]['id'])
    result['posts'] = posts
    result['posts_count'] = len(posts)

    cursor.execute(q2_followings)
    rows = cursor.fetchall()
    followings = [dict(zip(('id', 'username', 'you_followed_him', 'you_blocked_him'), row)) for row in rows]
    result['followings'] = followings
    result['followings_count'] = len(followings)

    cursor.execute(q3_followers)
    rows = cursor.fetchall()
    followers = [dict(zip(('id', 'username', 'you_followed_him', 'you_blocked_him'), row)) for row in rows]
    result['followers'] = followers
    result['followers_count'] = len(followers)

    cursor.execute(q4_username_and_bio)
    row = cursor.fetchone()
    result['username'] = row[0]
    result['bio'] = row[1]
    result['user_id'] = user_id

    if logged_in_user_id:
        q5_you_followed_him = """SELECT COUNT(*) FROM follows WHERE user_id = %s AND following_user_id = %s;""" % (logged_in_user_id, user_id)
        q6_you_blocked_him = """SELECT COUNT(*) FROM blocks WHERE user_id = %s AND blocked_user_id = %s;""" % (logged_in_user_id, user_id)
        cursor.execute(q5_you_followed_him)
        you_followed_him = cursor.fetchone()
        result['you_followed_him'] = you_followed_him[0]
        cursor.execute(q6_you_blocked_him)
        you_blocked_him = cursor.fetchone()
        result['you_blocked_him'] = you_blocked_him[0]

    return result


def get_post_hash_tags_query(post_id):
    q4_post_hash_tags = """SELECT id, hash_tag FROM hash_tags WHERE post_id = %s;""" % post_id
    cursor = get_database_connection()
    cursor.execute(q4_post_hash_tags)
    rows = cursor.fetchall()
    hash_tags = [dict(zip(('id', 'hash_tag'), row)) for row in rows]
    return hash_tags


def get_post_details_query(post_id, user_id):
    result = {}

    q1_post_detail = """SELECT posts.*, users.username 
    FROM posts 
    INNER JOIN users ON posts.user_id = users.id
    WHERE posts.id = %s;""" % post_id

    q2_post_likes = """SELECT posts_likes.user_id, users.username 
    FROM posts_likes 
    INNER JOIN users ON posts_likes.user_id = users.id
    WHERE posts_likes.post_id = %s;""" % post_id

    if user_id:
        q3_post_comments = """SELECT comments.id, comments.date, comments.context, comments.post_id, comments.user_id, comments.parent_id, users.username,
        (SELECT COUNT(*) FROM comments_likes WHERE comments_likes.comment_id = comments.id AND comments_likes.user_id = %s) 
        FROM comments 
        INNER JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = %s;""" % (user_id, post_id)
    else:
        q3_post_comments = """SELECT comments.id, comments.date, comments.context, comments.post_id, comments.user_id, comments.parent_id, users.username
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
    if user_id:
        comments = [dict(zip(('id', 'date', 'context', 'post_id', 'user_id', 'parent_id', 'user_username', 'has_current_user_liked'), row)) for row in rows]
    else:
        comments = [dict(zip(('id', 'date', 'context', 'post_id', 'user_id', 'parent_id', 'user_username'), row)) for row in rows]

    for i, _ in enumerate(comments):
        if comments[i]['parent_id'] is None:
            comments[i]['sub_comments'] = []
            for j, _ in enumerate(comments):
                if comments[j]['parent_id'] == comments[i]['id']:
                    comments[i]['sub_comments'].append(comments[j])
    for i, comment in enumerate(comments):
        if comment['parent_id'] is not None:
            del comments[i]

    result['post']['comments'] = comments
    result['post']['comments_count'] = len(comments)

    result['post']['hash_tags'] = get_post_hash_tags_query(post_id=post_id)

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


def search_username_query(username):
    pattern = '%'.join(username.strip().split())
    pattern = '%{}%'.format(pattern)
    query = """SELECT users.id, users.username FROM users WHERE (users.username ILIKE '{}') OR ('{}' LIKE '%' || users.username || '%');""".format(pattern, username)

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [dict(zip(('id', 'username'), row)) for row in rows]
    return users


def search_posts_containing_hash_tag_query(hash_tag, hash_tag_id, logged_in_user_id):
    if hash_tag:
        condition = "hash_tags.hash_tag = '#%s'" % hash_tag
    elif hash_tag_id:
        condition = "hash_tags.id = %s" % hash_tag_id
    else:
        return

    q1 = """SELECT posts.id, posts.date, posts.context, posts.user_id, users.username,
    (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id) AS likes_count, 
    (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id) AS comments_count
    FROM posts
    INNER JOIN users ON posts.user_id = users.id
    INNER JOIN hash_tags ON (posts.id = hash_tags.post_id) AND 
        (posts.user_id IN 
            (SELECT follows.following_user_id FROM follows WHERE follows.user_id = %s))
    WHERE %s;""" % (logged_in_user_id, condition)

    q2 = """SELECT posts.id, posts.date, posts.context, posts.user_id, users.username,
    (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id) AS likes_count, 
    (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id) AS comments_count
    FROM posts
    INNER JOIN users ON posts.user_id = users.id
    INNER JOIN hash_tags ON (posts.id = hash_tags.post_id) AND 
        (posts.user_id NOT IN 
            (SELECT follows.following_user_id FROM follows WHERE follows.user_id = %s)) AND 
        (posts.hash_tags_count = 2)
    WHERE %s
    ORDER BY posts.date DESC;""" % (logged_in_user_id, condition)

    q3 = """SELECT posts.id, posts.date, posts.context, posts.user_id, users.username,
    (SELECT COUNT(*) FROM posts_likes WHERE posts.id = posts_likes.post_id) AS likes_count, 
    (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id) AS comments_count
    FROM posts
    INNER JOIN users ON posts.user_id = users.id
    INNER JOIN hash_tags ON (posts.id = hash_tags.post_id) AND
        (posts.user_id NOT IN 
            (SELECT follows.following_user_id FROM follows WHERE follows.user_id = %s)) AND 
        (posts.hash_tags_count > 2)
    WHERE %s
    ORDER BY posts.hash_tags_count ASC;""" % (logged_in_user_id, condition)

    cursor = get_database_connection()
    cursor.execute(q1)
    rows = cursor.fetchall()
    cursor.execute(q2)
    rows += cursor.fetchall()
    cursor.execute(q3)
    rows += cursor.fetchall()
    posts = [dict(zip(('id', 'date', 'context', 'user_id', 'user_username', 'likes_count', 'comments_count'), row)) for row in rows]
    return posts


def get_most_likely_fraudulent_users_query():
    query = """SELECT users.id, users.username FROM users WHERE 
        ((SELECT COUNT(*) FROM posts WHERE users.id = posts.user_id) = 0 OR
        ((CURRENT_TIMESTAMP - (SELECT date FROM posts WHERE users.id = posts.user_id ORDER BY date LIMIT 1)) * 10 <= 
        (SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) * (INTERVAL '1 day')))
        AND 
        (2 * (SELECT COUNT(posts.user_id) AS liked_posts_of_a_user_count
        FROM posts 
        WHERE posts.id IN (SELECT posts_likes.post_id FROM posts_likes WHERE posts_likes.user_id = users.id)
        GROUP BY posts.user_id
        ORDER BY liked_posts_of_a_user_count DESC LIMIT 1) > (SELECT COUNT(posts_likes.id) FROM posts_likes WHERE posts_likes.user_id = users.id));"""

    cursor = get_database_connection()
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [dict(zip(('id', 'username'), row)) for row in rows]

    return users


def get_users_commented_more_than_10_times_under_more_than_3_posts_query():
    query = """SELECT users.id, users.username FROM users WHERE 
        (SELECT COUNT(*) FROM 
            (SELECT COUNT(comments.post_id) AS comments_count_in_each_post
                FROM comments 
                WHERE comments.user_id = users.id
                GROUP BY comments.post_id
            ) AS unique_posts
        WHERE comments_count_in_each_post > 10
        ) > 3;"""

    cursor = get_database_connection()
    cursor.execute(query)
    users = cursor.fetchall()
    return users


def get_question_for_logged_in_user_query(user_id):
    query = """SELECT questions.context
    FROM users 
    INNER JOIN questions ON questions.id = users.question_id
    WHERE users.id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(query)
    question_context = cursor.fetchone()
    return question_context[0]


def is_his_answer_correct_query(user_id, answer):
    query = """SELECT COUNT(*) FROM users WHERE id = %s AND answer = '%s';""" % (user_id, answer)

    cursor = get_database_connection()
    cursor.execute(query)
    is_his_answer_correct = cursor.fetchone()
    return True if is_his_answer_correct[0] == 1 else False


def get_forgotten_user_password_query(user_id):
    query = """SELECT password FROM users WHERE id = %s;""" % user_id

    cursor = get_database_connection()
    cursor.execute(query)
    password = cursor.fetchone()
    return password[0]


def does_his_old_password_match_query(user_id, old_password):
    query = """SELECT COUNT(*) FROM users WHERE id = %s AND password = '%s';""" % (user_id, old_password)

    cursor = get_database_connection()
    cursor.execute(query)
    does_his_old_password_match = cursor.fetchone()
    return True if does_his_old_password_match[0] == 1 else False


def change_user_password_query(user_id, new_password):
    query = """UPDATE users SET password = '%s' WHERE id = %s;""" % (new_password, user_id)

    cursor = get_database_connection()
    cursor.execute(query)
