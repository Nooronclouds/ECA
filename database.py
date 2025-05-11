import mysql.connector
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()  # Loads variables from .env

@contextmanager
def db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        yield conn
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_product_details(product_name):
    try:
        with db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT 
                        p.product_id, p.product_name, p.product_type,
                        b.brand_id, b.brand_name, b.is_affiliated, b.bds_report,
                        GROUP_CONCAT(c.country_name) AS countries
                    FROM Product p
                    JOIN Brand b ON p.brand_id = b.brand_id
                    LEFT JOIN BrandCountry bc ON b.brand_id = bc.brand_id
                    LEFT JOIN Country c ON bc.country_id = c.country_id
                    WHERE p.product_name LIKE %s
                    GROUP BY p.product_id
                """
                cursor.execute(query, (f"%{product_name}%",))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_product_details: {e}")
        return []

# Removed get_brand_history as the table doesn't exist in your schema
# Added proper error handling to add_alternative_product

def add_alternative_product(user_id, original_product_id, alt_name, alt_brand=None):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO AlternativeProduct 
                    (alt_product_name, afflicted_product_id, user_id, alt_brand_name)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (alt_name, original_product_id, user_id, alt_brand))
                conn.commit()
                return cursor.lastrowid
    except Exception as e:
        print(f"Error adding alternative product: {e}")
        return None