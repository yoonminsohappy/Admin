import pymysql
from connection import get_connection

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
    def get_property_id(self, seller_properties):
        QUERY = """
            SELECT
                id,
                name
            FROM seller_properties
            WHERE name = %s;
            """
        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor) #관계형 데이터베이스에 데이터를 키와 값으로 이루어지게 딕셔너리 형태로 만듦

        cursor.execute(QUERY, (seller_properties))
        result = cursor.fetchone() #row 가져옴

        cursor.close()
        db.close()

        return result['id'] if result else None 

    # seller삽입하기
    def insert_seller(self, user):
        QUERY = """
            INSERT INTO sellers
            (
                seller_status_id,
                seller_account,
                english_name,
                korean_name,
                cs_phone,
                seller_property_id,
                password
            ) 
            VALUES(1,%s, %s, %s, %s, %s, %s);
        """

        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor) 

        cursor.execute(QUERY, (user['seller_account'], user['english_name'],
            user['korean_name'], user['cs_phone'], user['seller_property_id'], user['password']))

        result = cursor.lastrowid

        cursor.close()
        db.commit()
        db.close()
        
        return result if result else None

    # seller_managers 삽입하기
    def insert_manager(self, manager):
        QUERY = """
            INSERT INTO seller_manager_tables
            (
               phone_number,
               seller_id
            ) 
            VALUES(%s, %s);
        """

        db     = get_connection(self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor) 

        cursor.execute(QUERY, (manager['phone_number'], manager['seller_id']))

        result = cursor.lastrowid

        cursor.close()
        db.commit()
        db.close()
        
        return result if result else None























    # 로그인
    # def select_seller(self, user):
    #     QUERY = """
    #         select
    #         (
    #             id,
    #             name,
    #             password 
    #         ) 
    #         from sellers;
    #     """

    #     db     = get_connection(self.db)
    #     cursor = db.cursor(pymysql.cursors.DictCursor) 

    #     cursor.execute(QUERY, (user['seller_account'], user['password']))

    #     result = cursor.lastrowid

    #     cursor.close()
    #     db.commit()
    #     db.close()
        
    #     return result if result else None

       