# import psycopg2
#
# def delete_all_tables(db_params):
#     try:
#         # Connect to the PostgreSQL database using db_params
#         connection = psycopg2.connect(**db_params)
#         connection.autocommit = True
#         cursor = connection.cursor()
#
#         # Fetch all table names in the 'public' schema
#         cursor.execute("""
#             SELECT tablename
#             FROM pg_tables
#             WHERE schemaname = 'public';
#         """)
#         tables = cursor.fetchall()
#
#         # Drop each table
#         for table in tables:
#             table_name = table[0]
#             cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
#             print(f'Table {table_name} deleted.')
#
#         print('All tables have been deleted.')
#
#     except Exception as error:
#         print(f"Error: {error}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print('Database connection closed.')
#
# # Your database connection parameters
# db_params = {
#     'dbname': 'os_dmdc',
#     'user': 'admin',
#     'password': 'mBwDpERHwVgoA81scRY34prcBXpeN2Sr',
#     'host': 'dpg-ctmsq69opnds73fidet0-a.oregon-postgres.render.com',
#     'port': 5432
# }
#
# # Call the function
# delete_all_tables(db_params)
