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
    def insert_sellers(self,db):
        sql = """
            INSERT INTO sellers
            (
                register_date,
                is_deleted
            ) 
            VALUES(default, default);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(sql, ())

        result = cursor.lastrowid
        cursor.close()

        return result if result else None

    def insert_seller_infomation(self, seller, db):
        sql = """
            INSERT INTO seller_informations
            (
                sellers_id,
                seller_account,
                password,
                seller_property_id,
                korean_name,
                english_name,
                cs_phone,
                modifier_id
            ) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(sql, (
            seller['sellers_id'],
            seller['seller_account'],
            seller['password'],
            seller['seller_property_id'],
            seller['korean_name'],
            seller['english_name'],
            seller['cs_phone'],
            seller['modifier_id']
        ))

        result = cursor.lastrowid
        cursor.close()
        
        return result if result else None

    # seller_managers 삽입하기
    def insert_manager(self, manager, db):
        sql = """
            INSERT INTO seller_managers
            (
               phone_number,
               sellers_id
            ) 
            VALUES(%s, %s);
        """
        cursor = db.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(sql, (manager['phone_number'], manager['sellers_id']))
        result = cursor.lastrowid #지금 인서트 된 아이다값을 가져옴

        cursor.close()
        db.commit()

        return result if result else None

    # 로그인
    def select_seller(self, seller_account , db):
        sql = """
            SELECT
                i.seller_account,
                i.password
            FROM seller_informations i
            INNER JOIN sellers s
                ON s.id = i.sellers_id
            WHERE i.seller_account=%s
            AND s.is_deleted != 1
            AND i.expired_at = '9999-12-31 23:59:59';
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
            INNER JOIN seller_informations i ON s.id = i.sellers_id
            INNER JOIN seller_properties p ON i.seller_property_id = p.id
            INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            INNER JOIN seller_managers m ON i.sellers_id = m.sellers_id
            WHERE s.id like %s
                AND i.seller_account like %s
                AND i.korean_name like %s
                AND i.english_name like %s
                AND t.name like %s
                AND p.name like %s
                AND m.name like %s
                AND m.phone_number like %s
                AND m.email like %s 
                AND s.is_deleted != 1
                AND i.expired_at = '9999-12-31 23:59:59'
            ORDER BY s.id DESC;
        """
               
                # AND i.seller_account like %s
                # AND i.korean_name like %s
                # AND i.english_name like %s
                # AND t.name like %s
                # AND p.name like %s
                # AND m.name like %s
                # AND m.phone_number like %s
                # AND m.email like %s                
            # "%" + search_info['seller_account'] +"%",
            # "%" + search_info['korean_name'] +"%", 
            # "%" + search_info['english_name'] +"%",
            # "%" + search_info['seller_status'] +"%",
            # "%" + search_info['seller_property'] +"%",
            # "%" + search_info['manager_name'] +"%",
            # "%" + search_info['manager_phone'] +"%",
            # "%" + search_info['manager_email'] +"%",
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
            "%" + search_info['manager_email'] +"%"
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
            i.seller_account as seller_account,
            i.english_name as english_name,
            i.korean_name as korean_name,
            m.name as manager_name,
            t.name as seller_status,
            m.phone_number as manager_phone_number,
            m.email as manager_email,
            p.name as seller_property,
            i.registered_product_count as registered_product_count,
            s.register_date as register_date
            FROM sellers s
            INNER JOIN seller_informations i ON s.id = i.sellers_id
            INNER JOIN seller_properties p ON i.seller_property_id = p.id
            INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            INNER JOIN seller_managers m ON s.id = m.sellers_id
            WHERE s.id like %s
                AND i.seller_account like %s
                AND i.korean_name like %s
                AND i.english_name like %s
                AND t.name like %s
                AND p.name like %s
                AND m.name like %s
                AND m.phone_number like %s
                AND m.email like %s
                AND i.expired_at = '9999-12-31 23:59:59'
                AND s.is_deleted != 1
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

    def find_seller_infomation(self, conn, id):

        sql = """
            SELECT *
            FROM seller_informations
            WHERE id = %s
        """

        #LIMIT : 최신데이터 한개만 뽑으려고(첫번째 인덱스 값을 1개 갖고오겠다는것) 
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (
            id
            ))
 
        results = cursor.fetchone()

        cursor.close()

        return results if results else None

    def insert_modification_history(self, conn, seller_info):

        sql = """
            INSERT INTO seller_status_modification_histories
            (
                sellers_id,
                updated_at,
                seller_status_id,
                modifier_id
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (
            seller_info['sellers_id'],
            seller_info['created_at'],
            seller_info['seller_status_id'],
            seller_info['modifier_id']
            ))

        results = cursor.lastrowid

        cursor.close()

        return results if results else None

