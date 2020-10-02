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
            AND
	            expired_at = '9999-12-31 23:59:59'
            ORDER BY korean_name ASC
            LIMIT %s;
        """
 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(sql, ("%" + search_term + "%", limit,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None


    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint
    
    #property_id 갖고오기
    def get_property_id(self, seller_properties, db):
        sql = """
            SELECT
                id,
                name
            FROM seller_properties
            WHERE name = %s;
            """
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, (seller_properties))
        result = cursor.fetchone() #row 가져옴
        cursor.close()

        return result if result else None


    # seller삽입하기
    def insert_seller(self,seller,db):
        sql = """
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
        cursor.execute(sql, (
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
        sql = """
            INSERT INTO seller_managers
            (
               phone_number,
               seller_id
            ) 
            VALUES(%s, %s);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(sql, (manager['phone_number'], manager['seller_id']))
        result = cursor.lastrowid #지금 인서트 된 아이다값을 가져옴

        cursor.close()
        db.commit()

        return result if result else None

    # 로그인
    def select_seller(self, seller_account , db):
        sql = """
            SELECT
                seller_account,
                password
            FROM sellers
            WHERE seller_account=%s;
        """  

        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, (seller_account))
        result = cursor.fetchone()
        cursor.close()

        return result if result else None

    def find_search_total_seller_list(self, conn, search_info):
        sql = """
            SELECT
            count(*) as count
            FROM sellers s
            INNER JOIN seller_properties p ON s.seller_property_id = p.id
            INNER JOIN seller_statuses t ON s.seller_status_id = t.id
            INNER JOIN seller_managers m ON s.id = m.seller_id
            WHERE s.id like %s       
                AND s.seller_account like %s
                AND s.korean_name like %s
                AND s.english_name like %s
                AND t.name like %s
                AND p.name like %s
                AND m.name like %s
                AND m.phone_number like %s
                AND m.email like %s
            ORDER BY s.id DESC
            ;
        """
#검색할때 조건을 여러개 주면 그 여러개에 대해서 and
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (
            "%" + search_info['id'] +"%",
            "%" + search_info['seller_account'] +"%",
            "%" + search_info['korean_name'] +"%", 
            "%" + search_info['english_name'] +"%",
            "%" + search_info['seller_status'] +"%",
            "%" + search_info['seller_property'] +"%",
            "%" + search_info['manager_name'] +"%",
            "%" + search_info['manager_phone'] +"%",
            "%" + search_info['manager_email'] +"%",
            ))
        
        # fetchone()은 한번 호출에 하나의 Row 만을 가져올 때 사용
        results = cursor.fetchone()['count']

        cursor.close()

        return results if results else None

    #셀러 검색
    def find_search_seller_list(self, conn, search_info):

        order = search_info['order']

        sql = """
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
            WHERE s.id like %s
                AND s.seller_account like %s
                AND s.korean_name like %s
                AND s.english_name like %s
                AND t.name like %s
                AND p.name like %s
                AND m.name like %s
                AND m.phone_number like %s
                AND m.email like %s
            ORDER BY s.id """ + order + """
            LIMIT %s, 10;
        """

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #쿼리에 검색 내용을 인자로 넣어서 실행
        #default가 ",  "%" + '' + "%" == "%%" 이다.
        #쿼리에 검색 내용을 인자로 넣어서 실행
        #default가 ",  "%" + '' + "%" == "%%" 이다.
        #and로 조건이 있으면 그 조건에 대해서 like로 찾고 없으면 like "%%" 닌깐 and연산에 영향이 없음
        #and로 하나씩 걸러서 조건에 맞는것만 가져온다.
        # %는 어떤 문자든지, 길이 상관없이 라는 의미!

        #쿼리에 검색 내용을 인자로 넣어서 실행
        cursor.execute(sql, (
            "%" + search_info['id'] +"%",
            "%" + search_info['seller_account'] +"%",
            "%" + search_info['korean_name'] +"%", 
            "%" + search_info['english_name'] +"%",
            "%" + search_info['seller_status'] +"%",
            "%" + search_info['seller_property'] +"%",
            "%" + search_info['manager_name'] +"%",
            "%" + search_info['manager_phone'] +"%",
            "%" + search_info['manager_email'] +"%",
            (int(search_info['page'])-1)*10
            ))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None