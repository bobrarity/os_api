import psycopg2
from psycopg2 import sql

from database import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD

db_params = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}


queries = [
    """
    """,
]

try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for query in queries:
        cursor.execute(query)

    conn.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
