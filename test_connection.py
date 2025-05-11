from database import db_connection

try:
    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            print("Tables in your database:", cursor.fetchall())
except Exception as e:
    print(f"Error testing connection: {e}")