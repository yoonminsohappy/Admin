import pymysql
from connection import get_connection

class SellerDao:
    def __init__(self, db):
        self.db = db

    def find_sellers_by_search_term(self, search_term, limit):
        QUERY = """
            SELECT 
                id, korean_name, profile_image, seller_property_id
            FROM 
                sellers
            WHERE 
                korean_name LIKE %s
            LIMIT %s;
            """

        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, ("%" + search_term + "%", int(limit),))
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results if results else None