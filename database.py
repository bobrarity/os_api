import asyncpg

DB_NAME = 'os'
DB_HOST = '192.168.0.118'
DB_PORT = '5432'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

db_conn = None


async def init_db_connection():
    global db_conn
    if db_conn is None:
        db_conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )


async def check_user_credentials(user_id, password):
    # global db_conn
    try:
        # if db_conn is None:
        #     await init_db_connection()

        # query = '''
        # SELECT COUNT(*) FROM auth
        # WHERE id = $1 AND auth_password = $2;
        # '''
        # result = await db_conn.fetchval(query, user_id, password)
        result = 'test'

        if not result:
            return False

        if str(user_id).startswith('S'):
            return 'staff'
        elif len(str(user_id)) == 7:
            return 'student'
        elif len(str(user_id)) == 5:
            return 'professor'
        else:
            return False

    except Exception as e:
        print(f'Error occurred while checking credentials for user_id {user_id}:', e)
        return False
