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
            2020-10-03(이충희): sellers 와 seller_informations의 테이블 분리로 쿼리문 변경
        """
        sql = """
            SELECT
                s.id, si.korean_name, si.profile_image, si.seller_property_id
            FROM 
                sellers AS s
            JOIN
                seller_informations AS si
            ON
                s.id = si.seller_id
            WHERE 
                si.korean_name LIKE %s
            AND
                si.expired_at = '9999-12-31 23:59:59'
            AND 
                s.is_deleted = 0
            ORDER BY korean_name ASC
            LIMIT %s;
        """
 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(sql, ("%" + search_term + "%", limit,))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None
 
    #property_id 갖고오기
    def get_property_id(self, conn, seller_properties):

        """
        회원가입시 sellr_property_id를 갖고 오기 위함, json데이터에서는 name으로만 준다.

        Args:
            conn             : 데이터베이스 커넥션 객체
            seller_properties: 셀러 속성 변수

        Returns:
            results: 셀러 속성 정보를 담은 row 하나
                {
                    "id": 샐러 속성 아이디,
                    "name" : 샐러 속성 명
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22.화(이지연) : 초기생성
            2020-10-04(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT
                    id,
                    name
                FROM seller_properties
                WHERE name = %s;
                """

            cursor.execute(sql, (seller_properties))
            result = cursor.fetchone() #row 가져옴
            #print(result)  -> {'id': 3, 'name': '로드샵'}

        return result if result else None    

    def get_status_id(self, conn, seller_status):

        """
        회원가입시 sellr_status_id를 갖고 오기 위함, json데이터에서는 name으로만 준다.

        Args:
            conn             : 데이터베이스 커넥션 객체
            seller_status: 셀러 상태 변수

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
                {
                    "id": 샐러 상태 아이디,
                    "name" : 샐러 속성 명
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22.화(이지연) : 초기생성
            2020-10-04(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql ="""
                SELECT
                    id,
                    name

                FROM seller_statuses

                WHERE name = %s;
            """

            cursor.execute(sql, (seller_status))
            result = cursor.fetchone() #row 가져옴

        return result if result else None

        def get_bank_id(self, conn, bank_name):
            """
            회원가입시 sellr_bank_id를 갖고 오기 위함, json데이터에서는 name으로만 준다.

            Args:
                conn             : 데이터베이스 커넥션 객체
                bank_name   : bank name을 담을 변수

            Returns:
                results: 셀러 은행 이름 정보를 담음
                    {
                        "id": 샐러 bank 아이디,
                        "name" : 샐러 bank 명
                    }

            Author:
                이지연(wldus9503@gmail.com)

            History:
                2020.09.22.화(이지연) : 초기생성
                2020-10-04(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
            """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql ="""
                SELECT
                    id,
                    name
                FROM banks
                WHERE name = %s;
            """

            #parameter 인자값 -> %s에 bank_name을 넣음
            cursor.execute(sql, (bank_name)) 
            result = cursor.fetchone() #row 가져옴
            cursor.close()

            return result if result else None

    # seller테이블 insert하기
    def insert_sellers(self,conn):

        """
        회원가입시 sellers테이블에 넣어줄 데이터

        Args:
            conn             : 데이터베이스 커넥션 객체

        Returns:
            results: sellers테이블에 정보를 담음
                {
                    "register_date": 가입일회원(defalut),
                    "is_deleted" : 삭제여부(defalut)
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020.10.04(이지연) : 데이터베이스 커서 with 문법 사용으로 변경 
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                INSERT INTO sellers
                (
                    register_date,
                    is_deleted
                ) 
                VALUES(default, default);
            """
            #sellers에 들어갈 값 -> defalut로 넣어줄 것이기 때문에 ()로 넣음
            cursor.execute(sql, ())

            #마지막으로 insert된 그 id값을 가져옴 -> 로직상에서 다른곳에서 쓰임
            #(예를 들어, 회원가입시 sellers에 두 값(register_date, is_deleted)을 넣어주고,
            # 그 id값을 fk로 sellers_informations과 같은 해당 sellers에 id값을 갖다 쓰기 위함)
            result = cursor.lastrowid

        return result if result else None

    def insert_seller_infomation(self, seller, conn):

        """
        회원가입시 sellers_information테이블에 넣어줄 데이터

        Args: 
            conn             : 데이터베이스 커넥션 객체
            seller           : 회원가입시에 넣어줄 데이터 변수

        Returns:
            results: 
                {
                    'seller_id'             : 셀러 고유 아이디,
                    'seller_account'        : 셀러 계정 아이디,
                    'password'              : 비밀번호,
                    'seller_property_id'    : 셀러 속성 아이디,
                    'korean_name'           : 셀러 한글 이름,
                    'english_name'          : 셀러 영어 이름,
                    'cs_phone'              : 고객센터 전화번호,
                    'modifier_id'           : 수정자 아이디,
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020-10-04(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                INSERT INTO seller_informations(
                    seller_id,
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

            cursor.execute(sql, (
                seller['seller_id'],
                seller['seller_account'],
                seller['password'],
                seller['seller_property_id'],
                seller['korean_name'],
                seller['english_name'],
                seller['cs_phone'],
                seller['modifier_id']
            ))

            result = cursor.lastrowid 
            
        return result if result else None

    # seller_managers 삽입하기
    def insert_manager(self, manager, conn):
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                INSERT INTO seller_managers(
                    name,
                    email, 
                    phone_number,
                    seller_id
                ) 
                VALUES(%s, %s, %s, %s);
            """

            cursor.execute(sql, (
                manager['manager_name'],
                manager['manager_email'],
                manager['manager_phone'],
                manager['seller_id']))

            result = cursor.lastrowid #지금 인서트 된 아이다값을 가져옴

        return result if result else None

    # 로그인
    def select_seller(self, seller_account , conn):

        """
        셀러 로그인 

        Args:
            conn             : 데이터베이스 커넥션 객체
            seller_status: 셀러 상태 변수

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
                {
                    "id": 샐러 상태 아이디,
                    "name" : 샐러 속성 명
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22.화(이지연) : 초기생성
            2020-10-5(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT
                    i.seller_id,
                    i.seller_account,
                    i.password,
                    i.is_master

                FROM seller_informations i

                INNER JOIN sellers s ON s.id = i.seller_id

                WHERE i.seller_account=%s

                AND s.is_deleted != 1 
                AND i.expired_at = '9999-12-31 23:59:59';
            """  
        # 로그인을 할때, 
        # 조건1)삭제된 회원이 아니다 
        # 조건2)최신의 정보만 갖고온다(아이디, 비밀번호 등)-> expired_at = 9999-12-31 23:59:59

            cursor.execute(sql, (seller_account))
            result = cursor.fetchone()

        return result if result else None
    
    # 셀러 검색 전체 갯수
    def find_search_total_seller_list(self, conn, search_info):

        """
        셀러 전체 검색 리스트 

        Args:
            conn             : 데이터베이스 커넥션 객체
            search_info      : 셀러 계정 아이디, 셀러 비밀번호를 담은 딕셔너리

        Returns:
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.05(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT
                count(*) as count
                
                FROM sellers s

                INNER JOIN seller_informations i ON s.id = i.seller_id
                INNER JOIN seller_properties p ON i.seller_property_id = p.id
                INNER JOIN seller_statuses t ON i.seller_status_id = t.id
                INNER JOIN seller_managers m ON i.seller_id = m.seller_id

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
            #검색할때 조건을 여러개 주면 그 여러개에 대해서 and

            # INNER JOIN seller_informations i ON s.id = i.seller_id   => 맨처음 s와 i를 조인시킨다.
            # INNER JOIN seller_properties p ON i.seller_property_id = p.id => 그 다음 아래줄 3개부터는 i와 조인가능한 것들을 해준다.
            # INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            # INNER JOIN seller_managers m ON i.seller_id = m.seller_id => 위에서 조인한 것을 i가 갖고있기 때문에 


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

            # like 구문에서 %:전체 단어, _:한단어 
            # %['']% => 모든 문자열 반환, null은 조건에 맞지 않아 반환하지 않는다.
            
            # fetchone()은 한번 호출에 하나의 Row 만을 가져올 때 사용
            results = cursor.fetchone()['count']

        return results if results else None

    #셀러 전체 리스트
    def find_search_seller_list(self, conn, search_info):
        """
        셀러 전체 리스트

        Args:
            conn             : 데이터베이스 커넥션 객체
            search_info      : 셀러 계정 아이디, 셀러 비밀번호를 담은 딕셔너리

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22.화(이지연) : 초기생성
            2020-10-5(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """

        # sql실행시킬 시 예약어로 인식을 하지 못하는 에러 때문에 미리 변수에 넣어서 sql문자열에 합쳐준다.
        order = search_info['order']
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

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

                INNER JOIN seller_informations i ON s.id = i.seller_id
                INNER JOIN seller_properties p ON i.seller_property_id = p.id
                INNER JOIN seller_statuses t ON i.seller_status_id = t.id
                INNER JOIN seller_managers m ON s.id = m.seller_id

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
            #LIMIT 시작점, 뽑을 갯수

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

        return results if results else None

    #검색 결과 리스트
    def find_seller_infomation(self, conn, id):
        """
        셀러 검색 결과 리스트 

        Args:
            conn             : 데이터베이스 커넥션 객체
            id               : 셀러 계정 아이디

        Returns:
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.05(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            sql = """
                SELECT *
                FROM seller_informations
                WHERE id = %s
            """

            cursor.execute(sql, (id))
            results = cursor.fetchone()

        return results if results else None

    #셀러 변경이력 기록
    def insert_modification_history(self, conn, seller_info):
        """
        변경이력 기록 insert하기

        Args:
            conn               : 데이터베이스 커넥션 객체
            result_seller      : 셀러 검색 결과 리스트 -> id

        Returns:
            results: 마지막 인서트 row 
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)  : 초기생성
            2020-10-5(이지연)     : 데이터베이스 커서 with 문법 사용으로 변경 
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                INSERT INTO seller_status_modification_histories
                (
                    seller_id,
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

            cursor.execute(sql, (
                seller_info['seller_id'],
                seller_info['created_at'],
                seller_info['seller_status_id'],
                seller_info['modifier_id']
                ))

            results = cursor.lastrowid

        return results if results else None

    #셀러 현재 기록 
    def find_seller(self, conn, id):
        
        """
        셀러 현재 기록된 데이터 갖고오기

        Args:
            conn    : 데이터베이스 커넥션 객체
            id      : 셀러 아이디

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)  : 초기생성
            2020-10-5(이지연): 데이터베이스 커서 with 문법 사용으로 변경 
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql ="""
                SELECT
                    si.seller_id as seller_id,
                    si.id as id,
                    seller_status_id,
                    seller_account,
                    english_name,
                    korean_name,
                    cs_phone,
                    seller_property_id,
                    profile_image,
                    password,
                    background_image,
                    simple_description,
                    detail_description,
                    zip_code,
                    address,
                    detail_address,
                    DATE_FORMAT(open_time,%s) as open_time,
                    DATE_FORMAT(close_time,%s) as close_time,
                    bank_id,
                    account_number,
                    account_name,
                    shipping_information,
                    exchange_refund_information,
                    model_height,
                    model_top_size,
                    model_bottom_size,
                    model_feet_size,
                    shopping_feedtext,
                    modifier_id,
                    DATE_FORMAT(created_at,%s) as created_at,
                    DATE_FORMAT(expired_at,%s) as expired_at,
                    is_master

                FROM sellers s

                INNER JOIN seller_informations si ON s.id = si.seller_id

                WHERE s.id = %s

                AND s.is_deleted != 1
                AND si.expired_at = '9999-12-31 23:59:59';
            """
            # 셀러가 삭제되지 않고, 선분이력종료일자가 '9999-12-31 23:59:59"로 최신의 데이터만 갖고오도록 함

            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (
                "%H:%i:%s",
                "%H:%i:%s",
                "%Y-%m-%d %H:%i:%s",
                "%Y-%m-%d %H:%i:%s",
                id
                ))
            result = cursor.fetchone() #row만

        return result if result else None

    #셀러 과거 정보를 삽입 
    def insert_past_seller_information(self, conn, past_seller_info):
        """
        셀러 과거 정보 insert하기

        Args:
            conn                  : 데이터베이스 커넥션 객체
            past_seller_info      : 과거 셀러 정보 

        Returns:
            results: 마지막 인서트 row 
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)  : 초기생성
            2020.10.05(이지연)     : 데이터베이스 커서 with 문법 사용으로 변경 
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        
            sql = """
                INSERT INTO
                seller_informations(
                    seller_id,
                    seller_status_id,
                    seller_account,
                    english_name,
                    korean_name,
                    cs_phone,
                    seller_property_id,
                    profile_image,
                    password,
                    background_image,
                    simple_description,
                    detail_description,
                    zip_code,
                    address,
                    detail_address,
                    open_time,
                    close_time,
                    bank_id,
                    account_number,
                    account_name,
                    shipping_information,
                    exchange_refund_information,
                    model_height,
                    model_top_size,
                    model_bottom_size,
                    model_feet_size,
                    shopping_feedtext,
                    modifier_id,
                    created_at,
                    expired_at,
                    is_master
                )
                VALUES(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s)
            """

            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (
                past_seller_info['seller_id'],
                past_seller_info['seller_status_id'],
                past_seller_info['seller_account'],
                past_seller_info['english_name'],
                past_seller_info['korean_name'],
                past_seller_info['cs_phone'],
                past_seller_info['seller_property_id'],
                past_seller_info['profile_image'],
                past_seller_info['password'],
                past_seller_info['background_image'],
                past_seller_info['simple_description'],
                past_seller_info['detail_description'],
                past_seller_info['zip_code'],
                past_seller_info['address'],
                past_seller_info['detail_address'],
                past_seller_info['open_time'],
                past_seller_info['close_time'],
                past_seller_info['bank_id'],
                past_seller_info['account_number'],
                past_seller_info['account_name'],
                past_seller_info['shipping_information'],
                past_seller_info['exchange_refund_information'],
                past_seller_info['model_height'],
                past_seller_info['model_top_size'],
                past_seller_info['model_bottom_size'],
                past_seller_info['model_feet_size'],
                past_seller_info['shopping_feedtext'],
                past_seller_info['modifier_id'],
                past_seller_info['created_at'],
                past_seller_info['is_master']    
            ))

            result = cursor.lastrowid

        return result if result else None
    
    #수정할 데이터로 update
    def update_seller_information(self, conn, updated_info, id):
        """
        셀러 정보 수정 하기

        Args:
            conn                  : 데이터베이스 커넥션 객체
            updated_info          : 셀러id값 가져온 후 updated_info에 추가한 값

        Returns:
            results: rowcount가 나온다.
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)     : 초기생성
            2020.10.05(이지연)     : 데이터베이스 커서 with 문법 사용으로 변경 
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            set_sql = ['created_at=now()']

            for key, value in updated_info.items():
                set_sql.append(key + "='" + str(value)+"'")
            
            set_sql = ", ".join(set_sql)
            # print(set_sql)
            # created_at=now(), seller_id='15', seller_status_id='3', seller_property_id='3', 
            # seller_account='star_0327', cs_phone='02-1342-2222', password='$2b$12$NM/tciULRV4vJuY8MnY0V.B87sUjjQ5Eqmu/SOtZ9LeHsqhkZRtvm',
            # profile_image='http://wecode11-brandi.s3.amazonaws.com/15_profile_image_cat1.jpg'
            
            sql ="""
                UPDATE
                    seller_informations
                SET
                    """ + set_sql + """
                WHERE id = %s
            """
            
            cursor.execute(sql, (id))

            result = cursor.rowcount

        return result if result else None

    #등록된 매니저를 삭제
    def delete_managers(self, conn, id):
        """
        셀러 정보 수정 하기

        Args:
            conn                  : 데이터베이스 커넥션 객체
            id                    : updated_info['seller_id']

        Returns:
            results: rowcount가 나온다.
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)     : 초기생성
            2020.10.05(이지연)     : 데이터베이스 커서 with 문법 사용으로 변경 
        """
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql ="""
                DELETE 
                FROM seller_managers
                WHERE seller_id = %s;
            """
            
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (id))

            result = cursor.rowcount

        return result if result else None

    #셀러 수정 페이지 seller에 관한 정보
    def find_detail_seller(self, conn, seller_id) :

        """
        셀러 수정 페이지를 위해 셀러의 정보를 가져온다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020-10-04(이지연): 초기 생성
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT
                    si.seller_id as seller_id,
                    si.id as id,
                    profile_image,
                    seller_status_id,
                    seller_property_id,
                    seller_account,
                    korean_name,
                    english_name,
                    cs_phone,
                    background_image,
                    password,
                    simple_description,
                    detail_description,
                    zip_code,
                    address,
                    detail_address,
                    DATE_FORMAT(open_time,%s) as open_time,
                    DATE_FORMAT(close_time,%s) as close_time,
                    bank_id,
                    account_number,
                    account_name,
                    shipping_information,
                    exchange_refund_information,
                    model_height,
                    model_top_size,
                    model_bottom_size,
                    model_feet_size,
                    shopping_feedtext,
                    modifier_id,
                    DATE_FORMAT(created_at,%s) as created_at,
                    DATE_FORMAT(expired_at,%s) as expired_at

                FROM sellers s

                INNER JOIN seller_informations si ON s.id = si.seller_id
                INNER JOIN seller_properties p ON si.seller_property_id = p.id
                INNER JOIN seller_statuses t ON si.seller_status_id = t.id   

                WHERE s.id = %s;
                
            """
            
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (
                "%H:%i:%s",
                "%H:%i:%s",
                "%Y-%m-%d %H:%i:%s",
                "%Y-%m-%d %H:%i:%s",
                seller_id
            ))

            results = cursor.fetchone()
            cursor.close()

        return results if results else None

    #셀러 수정 페이지 -> manager테이블 
    def find_detail_manager(self, conn, seller_id):

        """
        셀러 수정 페이지를 위해 셀러의 정보를 가져온다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함
        
        Returns:
            results: 셀러 정보를 담은 딕셔너리 리스트
                "manager":[
                            {
                                "email": "담당자 이메일",
                                "name":  "담당자 이름",
                                "phone_number": "담당자 전화번호"
                            },
                        ...(최대3까지)
         Author:
            이지연(wldus9503@gmail.com)

        History:
            2020-10-04(이지연): 초기 생성
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT 
                    m.name,
                    m.phone_number,
                    m.email

                FROM seller_managers m

                WHERE m.seller_id = %s 
                """

            cursor.execute(sql, (
                seller_id
            ))

            results = cursor.fetchall()

        return results if results else None

    #셀러 수정 페이지->셀러 정보 갖고오기
    def find_detail_seller_modification(self, conn, seller_id):

        """
        셀러 수정 페이지를 위해 셀러의 정보를 가져온다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함

        Returns:
            results: 셀러 정보 중 변경이력내용을 담은 딕셔너리 리스트
                "seller_modification":[
                    [1, "2020-10-03 22:25:26", "입점대기", "testa1234_1" ],
                     [1, "2020-10-03 22:25:26",…]
              }] 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020-10-04(이지연): 초기 생성
        """
        with conn.cursor() as cursor:  
            sql = """
                SELECT 
                    sm.seller_id as seller_id,
                    DATE_FORMAT(updated_at,%s) as updated_at,
                    t.name,
                    si.seller_account
                
                FROM seller_status_modification_histories sm
                
                INNER JOIN seller_statuses t ON sm.seller_status_id = t.id
                INNER JOIN seller_informations si ON sm.seller_id = si.seller_id
                
                WHERE sm.id = %s
                
                ORDER BY updated_at DESC
            """

            cursor.execute(sql, (
                "%Y-%m-%d %H:%i:%s",
                seller_id
            ))

            results = cursor.fetchall()

            return results if results else None