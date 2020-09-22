import pymysql
from flask import jsonify
from connection import get_connection

# 작성자: 김태수
# 수정일: 2020.09.21.월
# Product와 연결된 Class
class ProductDao:
    def __init__(self, db):
        self.db = db

    # 작성자: 김태수
    # 작성일: 2020.09.21.월
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
    def get_country_of_origin(self, country_id):
        try:
            db     = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT id, name
            FROM tests
            WHERE id = %s;
            """

            cursor.execute(sql, country_id)
            result = cursor.fetchone()
        except:
            db.rollback()
            raise
        else:
            db.commit()
            return result if result else None
        finally:
            cursor.close()
            db.close()

    def find_first_categories_by_seller_property_id(self, seller_property_id):
        QUERY = """
            SELECT 
                id, name
            FROM
                first_categories
            JOIN (
                SELECT 
                    first_category_id
                FROM
                    first_category_seller_properties
                WHERE
                    seller_property_id = %s
            ) as s
            ON
                first_categories.id = s.first_category_id;
            """

        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (int(seller_property_id),))
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results if results else None

    def find_second_categories_by_first_category_id(self, first_category_id):
        QUERY = """
            SELECT 
                id, name
            FROM
                second_categories
            JOIN (
                SELECT 
                    second_category_id
                FROM
                    first_category_second_categories
                WHERE
                    first_category_id = %s
            ) as s
            ON
                second_categories.id = s.second_category_id;
            """

        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (int(first_category_id),))
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results if results else None