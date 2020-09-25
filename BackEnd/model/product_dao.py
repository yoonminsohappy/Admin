import pymysql
from flask import jsonify
from connection import get_connection

class DAOInsertFailError(Exception):
    def __init__(self, message):
        super().__init__(message)


# 작성자: 김태수
# 수정일: 2020.09.21.월
# Product와 연결된 Class
class ProductDao:
    # 작성자: 김태수
    # 작성일: 2020.09.21.월
    # 원산지 데이터를 데이터베이스에서 가져오는 함수
    def get_country_of_origin(self, db, country_id):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT id, name
            FROM tests
            WHERE id = %s;
            """

            cursor.execute(sql, country_id)
            result = cursor.fetchone()
        except:
            raise
        else:
            return result if result else None
        finally:
            cursor.close()

    def find_first_categories_by_seller_property_id(self, conn, seller_property_id):
        QUERY = """
            SELECT
	            t2.id, t2.name 
            FROM 
	            first_category_seller_properties AS t1 
            LEFT JOIN 
	            first_categories AS t2 
            ON       
	            t1.first_category_id = t2.id 
            WHERE 
	            seller_property_id = %s;
            """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (seller_property_id,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None

    def find_second_categories_by_first_category_id(self, conn, first_category_id):
        QUERY = """
            SELECT
                t2.id, t2.name 
            FROM 
                first_category_second_categories AS t1 
            LEFT JOIN 
                second_categories AS t2 
            ON 
                t1.second_category_id = t2.id 
            WHERE 
                first_category_id = %s;
            """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (first_category_id,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None
        
    def find_categories_id(self, conn, first_category_id, second_category_id):
        QUERY = """
            SELECT 
                id
            FROM
                first_category_second_categories
            WHERE
                first_category_id = %s
            AND
                second_category_id = %s;
        """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(QUERY, (first_category_id, second_category_id,))
        result = cursor.fetchone()

        cursor.close()

        return result if result else None

    def create_product(self, conn, product_dict):
        QUERY = """
            INSERT INTO products (
                code,
                seller_id,
                categories_id
            ) VALUES (
                %(code)s,
                %(seller_id)s,
                %(categories_id)s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(QUERY, product_dict)
        if rows <= 0:
            raise pymysql.err.InternalError(10001, "DAO_COULD_NOT_INSERT_PRODUCT")

        result = cursor.lastrowid
        
        cursor.close()

        return result if result else None

    def create_product_detail(self, conn, product_detail_dict):
        QUERY = """
            INSERT INTO product_details (
                name,
                is_sold,
                is_displayed,
                origin_company,
                origin_date,
                simple_description,
                description,
                sale_price,
                discount_rate,
                discount_started_at,
                discount_ended_at,
                minimum_sale_amount,
                maximum_sale_amount,
                modifier_id,
                product_id,
                country_of_origin_id
            ) VALUES (
                %(name)s,
                %(is_sold)s,
                %(is_displayed)s,
                %(origin_company)s,
                %(origin_date)s,
                %(simple_description)s,
                %(description)s,
                %(sale_price)s,
                %(discount_rate)s,
                %(discount_started_at)s,
                %(discount_ended_at)s,
                %(minimum_sale_amount)s,
                %(maximum_sale_amount)s,
                %(modifier_id)s,
                %(product_id)s,
                %(country_of_origin_id)s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(QUERY, product_detail_dict)
        if rows <= 0:
            raise pymysql.err.InternalError(10002, "DAO_COULD_NOT_INSERT_PRODUCT_DETAIL")

        cursor.close()

    def create_product_image(self, conn, url, order, product_id):
        QUERY = """
            INSERT INTO product_images (
                image_path,
                ordering,
                product_id
            ) VALUES (
                %s,
                %s,
                %s
            );
        """
        cursor = conn.cursor()

        rows = cursor.execute(QUERY, (url, order, product_id,))
        if rows <= 0:
            raise pymysql.err.InternalError(10003, "DAO_COULD_NOT_INSERT_PRODUCT_IMAGE")

        cursor.close()

    def create_option(self, conn, option):
        QUERY = """
            INSERT INTO options (
                stock,
                color_id,
                size_id,
                product_id
            ) VALUES (
                %(stock)s,
                %(color_id)s,
                %(size_id)s,
                %(product_id)s
            );
        """
        cursor = conn.cursor()
        rows = cursor.execute(QUERY, option)
        if rows <= 0:
            raise pymysql.err.InternalError(10004, "DAO_COULD_NOT_INSERT_PRODUCT_OPTION")

        cursor.close()