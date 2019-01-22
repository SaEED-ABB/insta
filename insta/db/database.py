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


def create_user_query(**kwargs):
    int_columns = ['id', 'type']
    columns = "({})".format(','.join(kwargs.keys()))
    values = "({})".format(','.join([(value if column in int_columns else "'{}'".format(value)) for column, value in kwargs.items()]))
    query = """INSERT INTO users {} VALUES {};""".format(columns, values)

    cursor = get_database_connection()
    cursor.execute(query)


