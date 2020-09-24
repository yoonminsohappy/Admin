import pymysql

# from connection import get_connection
from flask      import jsonify

class SellerDao:
    def find_sellers_by_search_term(self, conn, search_term, limit):
        QUERY = """
            SELECT
                id, korean_name, profile_image, seller_property_id
            FROM 
                sellers
            WHERE 
                korean_name LIKE %s
            ORDER BY korean_name ASC
            LIMIT %s;
            """

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(QUERY, ("%" + search_term + "%", limit,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None


    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint
    
    #property_id 갖고오기
    def get_property_id(self, seller_properties, db):
        QUERY = """
            SELECT
                id,
                name
            FROM seller_properties
            WHERE name = %s;
            """
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(QUERY, (seller_properties))
        result = cursor.fetchone() #row 가져옴
        cursor.close()
        return result
        print(result)


    # seller삽입하기
    def insert_seller(self,seller,db):
        QUERY = """
            INSERT INTO sellers
            (
                seller_account,
                english_name,
                korean_name,
                cs_phone,
                seller_property_id,
                password
            ) 
            VALUES(%s, %s, %s, %s, %s, %s);
        """

        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(QUERY, (
            seller['seller_account'],
            seller['english_name'],
            seller['korean_name'],
            seller['cs_phone'],
            seller['seller_property_id'],
            seller['password']))

        result = cursor.lastrowid
        cursor.close()
        return result if result else None

    # seller_managers 삽입하기
    def insert_manager(self, manager, db):
        QUERY = """
            INSERT INTO seller_manager_tables
            (
               phone_number,
               seller_id
            ) 
            VALUES(%s, %s);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(QUERY, (manager['phone_number'], manager['seller_id']))
        result = cursor.lastrowid

        cursor.close()

        db.commit()
        db.close()
        
        return result if result else None


    # 로그인
    def select_seller(self, seller_account , db):
        QUERY = """
            SELECT
                seller_account,
                password
            FROM sellers
            WHERE seller_account=%s;
        """  

        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(QUERY, (seller_account))
        result = cursor.fetchone()
        
        cursor.close()
        return result
