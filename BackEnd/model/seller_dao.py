import pymysql

from flask      import jsonify

class SellerDao:
    def find_sellers_by_search_term(self, conn, search_term, limit):
        """
        상품 등록을 위해 셀러를 검색한다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            search_term: 검색어
            limit      : 몇 개의 row를 가져올지 정하는 수

        Returns:
            results: 셀러 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"                : 셀러 아이디,
                        "korean_name"       : 셀러 한글 이름,
                        "profile_image"     : 프로파일 이미지,
                        "seller_property_id": 샐러 속성 아이디
                    },
                    ...
                ] 

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-20(이충희): 초기 생성
            2020-09-23(이충희): 데이터베이스 커넥션 부분을 뷰 레벨로 이동시킴
        """
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

        return result

    # seller_managers 삽입하기
    def insert_manager(self, manager, db):
        QUERY = """
            INSERT INTO seller_managers
            (
               phone_number,
               seller_id
            ) 
            VALUES(%s, %s);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(QUERY, (manager['phone_number'], manager['seller_id']))
        result = cursor.lastrowid #지금 인서트 된 아이다값을 가져옴

        cursor.close()
        db.commit()

        return result

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

    #셀러 검색
    def find_search_seller_list(self, conn, search_keyword, search_value):
        #QUERY문에 WHERE 조건에 들어갈 키워드 삽입
        #이렇게 하는 이유 conn.execute를 통해서 쿼리를 실행할 때 %s를 통해서 인자로 넣어주는 경우 쿼리문에서 지정한 별칭과 연결되지 않아서 Syntax 에러가 발생하기때문에
        #미리 QUERY를 정의할 때 같이 넣어줘서 별칭을 인식할 수 있도록 하기 위해서
        QUERY = """
            SELECT
            s.id as id, 
            s.seller_account as seller_account,
            s.english_name as english_name,
            s.korean_name as korean_name,
            m.name as manager_name,
            t.name as seller_status,
            m.phone_number as manager_phone_number,
            m.email as manager_email,
            p.name as seller_property,
            s.registered_product_count as registered_product_count,
            s.register_date as register_date
            FROM sellers s
            INNER JOIN seller_properties p ON s.seller_property_id = p.id
            INNER JOIN seller_statuses t ON s.seller_status_id = t.id
            INNER JOIN seller_managers m ON s.id = m.seller_id
            WHERE """+ search_keyword +""" like %s;
        """
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #쿼리에 검색 내용을 인자로 넣어서 실행
        cursor.execute(QUERY, ("%" + search_value +"%")) 
        results = cursor.fetchall()

        cursor.close()

        return results
