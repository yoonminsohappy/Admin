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

        params = dict()

        params['seller_properties'] = seller_properties

        """
        회원가입시 sellr_property_id를 갖고 오기 위함 , json데이터에서는 name으로만 준다.

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
            2020.09.22(이지연) : 초기 생성
            2020.09.23(이지연) : 수정
                                -> view에서 db commit하도록 변경, 에러 처리 추가    
            2020.09.28(이지연)  : validation(유효성) 검사 삭제 -> ui쪽에서 처리하기로 결정
            2020.10.02(이지연)  : 모델링 변경 
                                -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020.10.04(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정
            2020.10.09(이지연)  :  모델링 param을 적용해 sql로직 수정

        """

        sql = """
                SELECT
                    id,
                    name
                FROM seller_properties
                WHERE name = %(seller_properties)s;
            """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))
            result = cursor.fetchone() #row 가져옴

            if not result:
                raise Exception("DATABASE IS NOT FOUND SELECT_PROPERTY_ID")

        return result

    def get_status_id(self, conn, seller_status):

        params = dict()

        params['seller_status'] = seller_status

        """
        회원가입시 sellr_status_id를 갖고 오기 위함, json데이터에서는 name으로만 준다.

        Args:
            conn             : 데이터베이스 커넥션 객체
            seller_status    : 셀러 상태 변수

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
                {
                    "id": 샐러 상태 아이디,
                    "name" : 샐러 속성 명
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기 생성
            2020.09.23(이지연) : 수정
                                -> view에서 db commit하도록 변경, 에러 처리 추가
            2020.09.25(이지연)  : 유효성 검사 추가
            2020.09.28(이지연)  : validation(유효성) 검사 삭제 -> ui쪽에서 처리하기로 결정
            2020.10.02(이지연)  : 모델링 변경 
                                -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020.10.04(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.07(이지연)  : 회원가입할 시 셀러 계정아이디, 셀러 cs_phone, manager_phone unique처리 추가
            2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정 
        """
        
        sql ="""
            SELECT
                id,
                name
            FROM seller_statuses
            WHERE name = %(seller_status)s;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))
            result = cursor.fetchone() #row 가져옴
            if not result:
                raise pymysql.err.InternalError("DATABASE IS NOT STATUS_ID")

        return result

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
                2020.09.22(이지연) : 초기생성
                2020.10.04(이지연) : 데이터베이스 커서 with 문법 사용으로 변경 
                2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정 

            """

            sql ="""
                SELECT
                    id,
                    name
                FROM banks
                WHERE name = %s;
            """

            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                #parameter 인자값 -> %s에 bank_name을 넣음
                cursor.execute(sql, (bank_name)) 
                result = cursor.fetchone() #row 가져옴
                cursor.close()

                if not result:
                    raise pymysql.err.InternalError('DATABASE IS NOT FOUND SELLER_BACNK_ID')
            return result

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
            2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정 

        """

        sql = """
            INSERT INTO sellers
            (
                register_date,
                is_deleted
            ) 
            VALUES(default, default);
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            #sellers에 들어갈 값 -> defalut로 넣어줄 것이기 때문에 ()로 넣음
            cursor.execute(sql, ())

            #마지막으로 insert된 그 id값을 가져옴 -> 로직상에서 다른곳에서 쓰임
            #(예를 들어, 회원가입시 sellers에 두 값(register_date, is_deleted)을 넣어주고,
            # 그 id값을 fk로 sellers_informations과 같은 해당 sellers에 id값을 갖다 쓰기 위함)
            result = cursor.lastrowid
            if not result:
                raise pymysql.err.InternalError(" DATABASE IS NOT FOUND INSERT SELLER")
        return result if result else None

    def insert_seller_infomation(self, seller, conn):

        """
        회원가입시 seller_information테이블에 넣어줄 데이터

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
            2020.09.22(이지연)  : 초기생성
            2020.10.02(이지연)  : 모델링 변경 
                                -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020.10-04(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.07(이지연)  : 쿼리 excute params 값 변경
            2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정 

        """

        params = dict()

        params['seller_id'] = seller['seller_id']
        params['seller_account'] = seller['seller_account']
        params['password'] = seller['password']
        params['seller_property_id'] = seller['seller_property_id']
        params['korean_name'] = seller['korean_name']
        params['english_name'] = seller['english_name']
        params['cs_phone'] = seller['cs_phone']
        params['modifier_id'] = seller['modifier_id']
        

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
            VALUES(
                %(seller_id)s,
                %(seller_account)s,
                %(password)s,
                %(seller_property_id)s,
                %(korean_name)s,
                %(english_name)s,
                %(cs_phone)s,
                %(modifier_id)s
                );
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
              params
            ))

            result = cursor.lastrowid 

            if not result:
                return pymysql.err.InternalError('DATABASE IS NOT FOUND INSERT SELLER_INFORMATION')
        return result

    # seller_managers 삽입하기
    def insert_manager(self, manager, conn):

        """
        회원가입시 seller_managers테이블에 넣어줄 데이터

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
                    'modifier_id'           : 수정자 아이디
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연)  : 초기생성
            2020.10.02(이지연)  : 모델링 변경 
                                -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
            2020.10-04(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.07(이지연)  : 쿼리 excute params 값 변경
            2020.10.08(이지연)  : 피드백 반영 팀원들과 형식 맞춰 수정

        """
        
        params = dict()

        params['name'] = manager['manager_name']
        params['email'] = manager['manager_email']
        params['phone_number'] = manager['manager_phone']
        params['seller_id'] = manager['seller_id']
    
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                INSERT INTO seller_managers(
                    name,
                    email, 
                    phone_number,
                    seller_id
                ) 
                VALUES(
                    %(name)s,
                    %(email)s,
                    %(phone_number)s,
                    %(seller_id)s
                    );
            """

            cursor.execute(sql, (
                    params
                ))

            result = cursor.lastrowid #지금 인서트 된 아이다값을 가져옴

            if not result:
                raise pymysql.err.InternalError('DATABASE IS NOT FOUND INSERT MANAGER')
        return result

    # 로그인
    def select_seller(self, seller_account, conn):

        params = dict()

        params['seller_account'] = seller_account

        """
        셀러 로그인 

        Args:
            conn                  : 데이터베이스 커넥션 객체
            seller_account        : 셀러 계정 아이디

        Returns:
            results: 셀러 상태 정보를 담은 row 하나
                {
                    "seller_account": 샐러 계정 아이디,
                    "name" : 샐러 속성 명
                }

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.05(이지연) : 데이터베이스 커서 with 문법 사용으로 변경 
            2020.10.07(이지연) : 쿼리 excute params 값 변경
            2020.10.08(이지연) : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연) : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        """

        sql = """
                SELECT
                    i.seller_id,
                    i.seller_account,
                    i.password,
                    i.is_master

                FROM seller_informations i

                INNER JOIN sellers s ON s.id = i.seller_id

                WHERE i.seller_account=%(seller_account)s

                AND s.is_deleted = 0 

                AND i.expired_at = '9999-12-31 23:59:59';
        """  
        
        # 로그인을 할때, 
        # 조건1)삭제된 회원이 아니다 
        # 조건2)최신의 정보만 갖고온다(아이디, 비밀번호 등)-> expired_at = 9999-12-31 23:59:59

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))
            result = cursor.fetchone()

            if not result:
                raise Exception('DATABASE IS NOT SELECT SELLER')
        return result
    
    # 셀러 검색 전체 갯수 - 조건에 맞는 총 개수 구함
    def find_search_total_seller_list(self, conn, search_info):
        """
        셀러 검색 전체 갯수

        Args:
            conn             : 데이터베이스 커넥션 객체
            search_info      : 셀러 계정 아이디, 셀러 비밀번호를 담은 딕셔너리

        Returns:
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.09.22(이지연) : 초기생성
            2020.10.05(이지연) : 데이터베이스 커서 with 문법 사용으로 변경 
            2020.10.07(이지연) : 쿼리문 수정 -> PARAM으로 먼저 값이 있는 지 확인 후 추가, sql 컬럼 별칭 달기
            2020.10.08(이지연) : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연) : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        """ 
               
        params = dict()

        params = {
            'id':None, 
            'seller_account':None, 
            'korean_name':None,
            'english_name':None,
            'seller_status':None,
            'seller_property':None,
            'manager_name':None,
            'manager_phone':None,
            'manager_email':None,
            'start_date':None,
            'end_date':None
        }

        if search_info['id']:
            params['id'] = search_info['id']

        if search_info['seller_account']:
            params['seller_account'] = "%" + search_info['seller_account'] +"%"

        if search_info['korean_name']:
            params['korean_name'] = "%" + search_info['korean_name'] +"%"

        if search_info['english_name']:
            params['english_name'] = "%" + search_info['english_name'] +"%"

        if search_info['seller_status']:
            params['seller_status'] = "%" + search_info['seller_status'] +"%"
        
        if search_info['seller_property']:
            params['seller_property'] = "%" + search_info['seller_property'] +"%"
        
        if search_info['manager_name']:
            params['manager_name'] = "%" + search_info['manager_name'] +"%"

        if search_info['manager_phone']:
            params['manager_phone'] = "%" + search_info['manager_phone'] +"%"

        if search_info['manager_email']:
            params['manager_email'] = "%" + search_info['manager_email'] +"%"   

        if search_info['start_date']:
            params['start_date'] = search_info['start_date']

        if search_info['end_date']:
            params['end_date'] = search_info['end_date']

        where_sql = ""

        if params['id']:
            where_sql += """
                AND
                    i.seller_id = %(id)s
            """

        if params['seller_account']:
            where_sql += """
                AND
                    i.seller_account like %(seller_account)s
            """

        if params['korean_name']:
            where_sql += """
                AND 
                    i.korean_name like %(korean_name)s
            """
        
        if params['english_name']:
            where_sql += """
                AND 
                    i.english_name like %(english_name)s
            """

        if params['manager_phone']:
            where_sql += """
                AND 
                    m.phone_number like %(manager_phone)s
            """

        if params['manager_email']:
            where_sql += """
                AND 
                    m.email like %(manager_email)s
            """

        if params['start_date'] and params['end_date']:
            where_sql += """
                AND
                    s.register_date BETWEEN %(start_date)s and %(end_date)s
            """
        
        sql = """
            SELECT
                count(*) as count
            
            FROM sellers s

            INNER JOIN seller_informations i ON s.id = i.seller_id
            INNER JOIN seller_properties p ON i.seller_property_id = p.id
            INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            INNER JOIN seller_managers m ON i.seller_id = m.seller_id

            WHERE s.is_deleted = 0
            AND i.expired_at = '9999-12-31 23:59:59'
                """ + where_sql + """;
        """
            #검색할때 조건을 여러개 주면 그 여러개에 대해서 and

            # INNER JOIN seller_informations i ON s.id = i.seller_id   => 맨처음 s와 i를 조인시킨다.
            # INNER JOIN seller_properties p ON i.seller_property_id = p.id => 그 다음 아래줄 3개부터는 i와 조인가능한 것들을 해준다.
            # INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            # INNER JOIN seller_managers m ON i.seller_id = m.seller_id => 위에서 조인한 것을 i가 갖고있기 때문에 
        #print(sql)
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(sql, (
                    params
                ))

            # like 구문에서 %:전체 단어, _:한단어 
            # %['']% => 모든 문자열 반환, null은 조건에 맞지 않아 반환하지 않는다.
            
            results = cursor.fetchone()['count']

            if not results:
                raise pymysql.err.InternalError("DATABASE IS NOT FIND_SEARCH TOTAL SELLER LIST")
        return results 

    #셀러 전체 리스트
    def find_search_seller_list(self, conn, search_info):

        """
        셀러 전체 리스트

        Args:
            conn             : 데이터베이스 커넥션 객체
            search_info      : 셀러 데이터를 담은 리스트

        Returns:
            results: fetchall()을 이용하여 셀러 상태 정보를 모두 리턴
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)  : 초기 생성
            2020.10.05(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경 
            2020.10.07(이지연)  : 쿼리 excute params 값 변경 
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경

        """

        params = dict()

        params = {
            'id':None, 
            'seller_account':None, 
            'korean_name':None,
            'english_name':None,
            'seller_status':None,
            'seller_property':None,
            'manager_name':None,
            'manager_phone':None,
            'manager_email':None,
            'start_date':None,
            'end_date':None,
            'register_date': "%Y-%m-%d %H:%i:%s"
        }

        if search_info['id']:
            params['id'] = "%" + search_info['id'] +"%"

        if search_info['seller_account']:
            params['seller_account'] = "%" + search_info['seller_account'] +"%"

        if search_info['korean_name']:
            params['korean_name'] = "%" + search_info['korean_name'] +"%"

        if search_info['english_name']:
            params['english_name'] = "%" + search_info['english_name'] +"%"

        if search_info['seller_status']:
            params['seller_status'] = "%" + search_info['seller_status'] +"%"
        
        if search_info['seller_property']:
            params['seller_property'] = "%" + search_info['seller_property'] +"%"
        
        if search_info['manager_name']:
            params['manager_name'] = "%" + search_info['manager_name'] +"%"

        if search_info['manager_phone']:
            params['manager_phone'] = "%" + search_info['manager_phone'] +"%"

        if search_info['manager_email']:
            params['manager_email'] = "%" + search_info['manager_email'] +"%"

        if search_info['start_date']:
            params['start_date'] = search_info['start_date']

        if search_info['end_date']:
            params['end_date'] = search_info['end_date']

        params['page'] = (int(search_info['page'])-1)*10
        params['per_page'] = search_info['per_page']

        order = search_info['order']

        # order의 경우 sql실행시킬 시 예약어로 인식을 하지 못하는 에러 때문에 미리 변수에 넣어서 sql문자열에 합쳐준다.

        where_sql = ""

        if params['id']:
            where_sql += """
                AND
                    s.id = %(id)s
                """

        if params['seller_account']:
            where_sql += """
                AND
                    i.seller_account like %(seller_account)s
                """
        
        if params['english_name']:
            where_sql += """
                AND i.english_name like %(english_name)s
            """

        if params['korean_name']:
            where_sql += """
                AND 
                    i.korean_name like %(korean_name)s
            """

        if params['manager_name']:
            where_sql +=  """
                AND
                    m.name like %(manager_name)s
            """
        
        if params['seller_status']:
            where_sql += """
                AND 
                    t.name like %(seller_status)s
            """

        if params['manager_phone']:
            where_sql += """
                AND 
                    phone_number like %(manager_phone)s
                """

        if params['manager_email']:
            where_sql += """
                AND 
                    t.name like %(manager_email)s
                """

        if params['seller_property']:
            where_sql += """
                AND
                    p.name like %(seller_property)s
                """

        if params['start_date']  and params['end_date']:
            where_sql += """
                AND
                    s.register_date BETWEEN %(start_date)s and %(end_date)s
                """

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
                DATE_FORMAT(s.register_date,%(register_date)s) as register_date

            FROM sellers s

            INNER JOIN seller_informations i ON s.id = i.seller_id
            INNER JOIN seller_properties p ON i.seller_property_id = p.id
            INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            INNER JOIN seller_managers m ON s.id = m.seller_id

            WHERE s.is_deleted = 0
            AND i.expired_at = '9999-12-31 23:59:59'
                """ + where_sql + """

            ORDER BY id """ + order + """
            
            LIMIT %(page)s, %(per_page)s;
        """
            #LIMIT 시작점, 뽑을 갯수
            #쿼리에 검색 내용을 인자로 넣어서 실행
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
                ))
            results = cursor.fetchall()
            
            if not results:
                raise pymysql.err.InternalError('DATABASE IS NOT SELECT FIND SEARCH SELLER LIST')

        return results

    #셀러 상세 정보 찾기(셀러 information pk값으로 찾는다.)
    def find_seller_infomation(self, conn, id):
        """
        셀러 상세 데이터 리스트 

        Args:
            conn             : 데이터베이스 커넥션 객체
            id               : 셀러 계정 아이디

        Returns:
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연) : 초기생성
            2020.10.05(이지연) : 데이터베이스 커서 with 문법 사용으로 변경 
            2020.10.07(이지연) : 쿼리 excute params 값 변경 

        """
        params = dict()

        params['id'] = id

        sql = """
            SELECT *
            FROM seller_informations
            WHERE id = %(id)s
            
            """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
                ))
            results = cursor.fetchone()
            if not results:
                raise pymysql.err.InternalError('NOT FOUND SELECT SELLER INFORMATION')

        return results if results else None

    #셀러 변경이력 기록
    def insert_modification_history(self, conn, seller_info):
        """
        변경이력 기록 insert하기

        Args:
            conn               : 데이터베이스 커넥션 객체
            seller_info        : 셀러 데이터 리스트

        Returns:
            results: 마지막 인서트 row 
    
        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.04(이지연)     : 초기생성
            2020-10-5(이지연)      : 데이터베이스 커서 with 문법 사용으로 변경 
            2020.10.07(이지연)     : 쿼리 excute params 값 변경 

        """
        params = dict()

        params['seller_id'] = seller_info['seller_id']
        params['updated_at'] = seller_info['created_at']
        params['seller_status_id'] = seller_info['seller_status_id']
        params['modifier_id'] = seller_info['modifier_id']

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
                %(seller_id)s,
                %(updated_at)s,
                %(seller_status_id)s,
                %(modifier_id)s
            )
            """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))

            results = cursor.lastrowid
            if not results:
                raise Exception('DATABASE IS NOT FOUND LASTROWID')
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
            2020.10.05(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.07(이지연)  : 쿼리 excute params 값 변경 

        """

        params = dict()

        params['seller_id'] = id
        params['open_time'] = "%H:%i:%s"
        params['close_time'] = "%H:%i:%s"
        params['created_at'] = "%Y-%m-%d %H:%i:%s"
        params['expired_at'] = "%Y-%m-%d %H:%i:%s"

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
                DATE_FORMAT(open_time,%(open_time)s) as open_time,
                DATE_FORMAT(close_time,%(close_time)s) as close_time,
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
                DATE_FORMAT(created_at,%(created_at)s) as created_at,
                DATE_FORMAT(expired_at,%(expired_at)s) as expired_at,
                is_master

            FROM sellers s

            INNER JOIN seller_informations si ON s.id = si.seller_id

            WHERE s.id = %(seller_id)s

            AND s.is_deleted = 0
            AND si.expired_at = '9999-12-31 23:59:59';
        """
        # 셀러가 삭제되지 않고, 선분이력종료일자가 '9999-12-31 23:59:59"로 최신의 데이터만 갖고오도록 함

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, (
                params
                ))
            result = cursor.fetchone() #row만
            if not result:
                raise Exception('DATABASE IS NOT SELECT FIND SELLER')
        return result

    #셀러 과거 정보를 삽입 
    def insert_past_seller_information(self, conn, past_seller_info):

        params = dict()

        params['seller_id'] = past_seller_info['seller_id']
        params['seller_status_id'] = past_seller_info['seller_status_id']
        params['seller_account'] = past_seller_info['seller_account']
        params['english_name'] = past_seller_info['english_name']
        params['korean_name'] = past_seller_info['korean_name']
        params['cs_phone'] = past_seller_info['cs_phone']
        params['seller_property_id'] = past_seller_info['seller_property_id']
        params['profile_image'] = past_seller_info['profile_image']
        params['password'] = past_seller_info['password']
        params['background_image'] = past_seller_info['background_image']
        params['simple_description'] = past_seller_info['simple_description']
        params['detail_description'] = past_seller_info['detail_description']
        params['zip_code'] = past_seller_info['zip_code']
        params['address'] = past_seller_info['address']
        params['detail_address'] = past_seller_info['detail_address']
        params['open_time'] = past_seller_info['open_time']
        params['close_time'] = past_seller_info['close_time']
        params['bank_id'] = past_seller_info['bank_id']
        params['account_number'] = past_seller_info['account_number']
        params['account_name'] = past_seller_info['account_name']
        params['shipping_information'] = past_seller_info['shipping_information']
        params['exchange_refund_information'] = past_seller_info['exchange_refund_information']
        params['model_height'] = past_seller_info['model_height']
        params['model_top_size'] = past_seller_info['model_top_size']
        params['model_bottom_size'] = past_seller_info['model_bottom_size']
        params['model_feet_size'] = past_seller_info['model_feet_size']
        params['shopping_feedtext'] = past_seller_info['shopping_feedtext']
        params['modifier_id'] = past_seller_info['modifier_id']
        params['created_at'] = past_seller_info['created_at']
        params['expired_at'] = past_seller_info['expired_at']
        params['is_master'] = past_seller_info['is_master']

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
            2020.10.05(이지연)  : 데이터베이스 커서 with 문법 사용으로 변경
            2020.10.07(이지연)  : 쿼리 excute params 값 변경 
        """
    
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
                %(seller_id)s, 
                %(seller_status_id)s,
                %(seller_account)s,
                %(english_name)s,
                %(korean_name)s,
                %(cs_phone)s,
                %(seller_property_id)s,
                %(profile_image)s,
                %(password)s,
                %(background_image)s,
                %(simple_description)s,
                %(detail_description)s,
                %(zip_code)s,
                %(address)s,
                %(detail_address)s,
                %(open_time)s,
                %(close_time)s,
                %(bank_id)s,
                %(account_number)s,
                %(account_name)s, 
                %(shipping_information)s,
                %(exchange_refund_information)s,
                %(model_height)s,
                %(model_top_size)s,
                %(model_bottom_size)s,
                %(model_feet_size)s,
                %(shopping_feedtext)s,
                %(modifier_id)s,
                %(created_at)s,
                now(),
                %(is_master)s
                )
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))

            result = cursor.lastrowid
            if not result:
                raise Exception('DATABASE IS NOT FOUND LASTROWID')
        return result
    
    #수정할 데이터로 update
    def update_seller_information(self, conn, updated_info, id):

        params = dict()

        params['seller_id'] = id

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
        set_sql = ['created_at=now()']

        for key, value in updated_info.items():
            set_sql.append(key + "='" + str(value)+"'")
        
        set_sql = ", ".join(set_sql)

            # created_at=now(), seller_id='15', seller_status_id='3', seller_property_id='3', 
            # seller_account='star_0327', cs_phone='02-1342-2222', password='$2b$12$NM/tciULRV4vJuY8MnY0V.B87sUjjQ5Eqmu/SOtZ9LeHsqhkZRtvm',
            # profile_image='http://wecode11-brandi.s3.amazonaws.com/15_profile_image_cat1.jpg'
            
        sql ="""
            UPDATE
                seller_informations
            SET
                """ + set_sql + """
            WHERE id = %(seller_id)s;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            
            cursor.execute(sql, (
                params
                ))

            result = cursor.rowcount
            if result <= 0 or not result:
                raise Exception('DATABASE IS NOT FOUND ROWCOUNT')
        return result

    #등록된 매니저를 삭제
    def delete_managers(self, conn, id):

        params = dict()

        params['seller_id'] = id

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
        
        sql ="""
            DELETE 
            FROM seller_managers
            WHERE seller_id = %(seller_id)s;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(sql, (
                params
                ))

            result = cursor.rowcount
            if result <= 0 or not result:
                raise pymysql.err.InternalError('SQL DELETE FAILED')
        return result

    #셀러 수정 페이지 seller에 관한 정보
    def find_detail_seller(self, conn, seller_id) :

        params = dict()

        params['seller_id'] = seller_id
        params['open_time'] = "%H:%i:%s"
        params['close_time'] = "%H:%i:%s"
        params['created_at'] = "%Y-%m-%d %H:%i:%s"
        params['expired_at'] = "%Y-%m-%d %H:%i:%s"

        """
        셀러 수정 페이지를 위해 셀러의 정보를 가져온다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020-10-04(이지연): 초기 생성
            2020-10-06(이지연): error발생시 raise처리
        """

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
                DATE_FORMAT(open_time,%(open_time)s) as open_time,
                DATE_FORMAT(close_time,%(close_time)s) as close_time,
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
                DATE_FORMAT(created_at,%(created_at)s) as created_at,
                DATE_FORMAT(expired_at,%(expired_at)s) as expired_at

            FROM sellers s

            INNER JOIN seller_informations si ON s.id = si.seller_id
            INNER JOIN seller_properties p ON si.seller_property_id = p.id
            INNER JOIN seller_statuses t ON si.seller_status_id = t.id   

            WHERE s.id = %(seller_id)s ;
            
        """
            
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.execute(sql, (
                params
            ))

            results = cursor.fetchone()
            if not results:
                raise Exception("DB ERROR OCCURS AND NOT FOUND SELLER_INFORMATION")

        return results

    #셀러 수정 페이지 -> manager테이블 
    def find_detail_manager(self, conn, seller_id):
        
        params = dict()

        params['seller_id'] = seller_id

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
            2020-10-06(이지연): error발생시 raise처리

        """
        sql = """
            SELECT 
                m.name,
                m.phone_number,
                m.email

            FROM seller_managers m

            WHERE m.seller_id = %(seller_id)s ;
            """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
            ))

            results = cursor.fetchall()

            if not results:
                raise Exception("DATABASE IS NOT FOUND DETAIL_MANAGER")

        return results

    #셀러 수정 페이지->셀러 정보 갖고오기
    def find_detail_seller_modification(self, conn, seller_id):
        
        params = dict()

        params['seller_id'] = seller_id
        params['updated_time'] = "%Y-%m-%d %H:%i:%s"

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
            2020.10.04(이지연) : 초기 생성
            2020.10.06(이지연) : error발생시 raise처리
            2020.10.07(이지연) : 회원가입할 시 셀러 계정아이디, 셀러 cs_phone, manager_phone unique처리 추가
        
        """
        
        sql = """
            SELECT 
                sm.seller_id as seller_id,
                DATE_FORMAT(updated_at,%(updated_time)s) as updated_time,
                t.name,
                si.seller_account
            
            FROM seller_status_modification_histories sm
            
            INNER JOIN seller_statuses t ON sm.seller_status_id = t.id
            INNER JOIN seller_informations si ON sm.seller_id = si.seller_id
            
            WHERE sm.seller_id = %(seller_id)s
            AND si.expired_at = '9999-12-31 23:59:59'
            
            ORDER BY updated_time DESC
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchall()

            if not results:
                raise Exception("DATABASE IS NOT FOUND DETAIL_MODIFICATION_DATA")
            return results

    #데코레이터 seller_id 
    def decorator_find_seller(self, conn, seller_id):
        """
        셀러 id를 이용한 데코레이터 함수 

        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함

        Returns:
            results: 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.08(이지연) : 초기 생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        
        """
        params = dict()

        params['seller_id'] = seller_id

        sql = """
            SELECT 
                i.seller_id,
                i.seller_account,
                i.is_master,
                i.cs_phone
                
            FROM seller_informations i

            INNER JOIN sellers s ON s.id = i.seller_id
            
            WHERE seller_id = %(seller_id)s
            
            AND s.is_deleted = 0 

            AND i.expired_at = '9999-12-31 23:59:59'
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchone()
            if not results:
                raise Exception("DATABASE IS NOT FOUND USER")
            return results

    def unique_seller_account(self, conn, seller_account):
        """
        셀러 계정아이디 unique처리를 하여 회원가입시 중복되지 않도록 한다.

        Args:
            conn            : 데이터베이스 커넥션 객체
            seller_account  : 셀러 계정 아이디

        Returns:
            results: 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.07(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        
        """

        params = dict()

        params['seller_account'] = seller_account

        sql = """
            SELECT 
                count(*) as count
            
            FROM seller_informations i

            INNER JOIN sellers s ON s.id = i.seller_id
            
            WHERE i.seller_account = %(seller_account)s

            AND s.is_deleted = 0 

            AND i.expired_at = '9999-12-31 23:59:59'
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchone()

            if not results:
                raise Exception("DATABASE IS NOT FOUND SELECT SELLER ACOOUNT")
            return results['count']

    def unique_cs_phone(self, conn, cs_phone):
        """
        셀러 cs 전화번호를 unique처리를 하여 회원가입시 중복되지 않도록 한다.

        Args:
            conn            : 데이터베이스 커넥션 객체
            cs_phone        : cs전화번호

        Returns:
            results: 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.07(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        
        """

        params = dict()

        params['cs_phone'] = cs_phone

        sql = """
            SELECT 
                count(*) as count
            
            FROM seller_informations i

            INNER JOIN sellers s ON s.id = i.seller_id
            
            WHERE cs_phone = %(cs_phone)s

            AND s.is_deleted = 0

            AND i.expired_at = '9999-12-31 23:59:59'
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchone()

            if not results:
                raise Exception("DATABASE IS NOT FOUND SELECT_CSPHONE")
            return results['count']

    def unique_manager_phone(self, conn, phone_number):
        """
        셀러 담당자 전화번호를 unique처리를 하여 회원가입시 중복되지 않도록 한다.

        Args:
            conn                : 데이터베이스 커넥션 객체
            phone_number        : 담당자 전화번호

        Returns:
            results: 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.07(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        
        """

        params = dict()

        params['phone_number'] = phone_number

        sql = """
            SELECT 
                count(*) as count
            
            FROM seller_managers
            
            WHERE phone_number = %(phone_number)s
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchone()

            if not results:
                raise Exception("DATABASE IS NOT FOUND SELECT MAANGER_PHONE")
            return results['count']

    def unique_manager_email(self, conn, email):
        """
        셀러 담당자 이메일을 unique처리를 하여 회원가입시 중복되지 않도록 한다.

        Args:
            conn                 : 데이터베이스 커넥션 객체
            manager_email        : 담당자 이메일

        Returns:
            results: 

        Author:
            이지연(wldus9503@gmail.com)

        History:
            2020.10.07(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경
        
        """

        params = dict()

        params['email'] = email

        sql = """
            SELECT 
                count(*) as count
            
            FROM seller_managers
            
            WHERE email = %(email)s
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:          
            cursor.execute(sql, (
                params
            ))
            results = cursor.fetchone()

            if not results:
                raise Exception("DATABASE IS NOT FOUND SELECT MANAGER_EMAIL")
            return results['count']

    #셀러 엑셀 전체 리스트
    def find_search_seller_list_excel(self, conn, search_info):
        """
        엑셀 다운로드 파일 엔드포인트

        Args: 
            conn        : 데이터베이스 커넥션 객체
            search_info : 검색 결과 정보를 담을 리스트

        Retruns:
            400, {'message': 'UNSUCCESS'} 

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020.10.09(이지연) : 초기 설정
            2020.10.11(이지연) : user_id 중복 발생으로 인한 에러 수정
            
    """
        params = dict()

        params = {
            'id':None, 
            'seller_account':None, 
            'korean_name':None,
            'english_name':None,
            'seller_status':None,
            'seller_property':None,
            'manager_name':None,
            'manager_phone':None,
            'manager_email':None,
            'start_date':None,
            'end_date':None,
            'register_date': "%Y-%m-%d %H:%i:%s"
        }

        if search_info['id']:
            params['id'] = "%" + search_info['id'] +"%"

        if search_info['seller_account']:
            params['seller_account'] = "%" + search_info['seller_account'] +"%"

        if search_info['korean_name']:
            params['korean_name'] = "%" + search_info['korean_name'] +"%"

        if search_info['english_name']:
            params['english_name'] = "%" + search_info['english_name'] +"%"

        if search_info['seller_status']:
            params['seller_status'] = "%" + search_info['seller_status'] +"%"
        
        if search_info['seller_property']:
            params['seller_property'] = "%" + search_info['seller_property'] +"%"
        
        if search_info['manager_name']:
            params['manager_name'] = "%" + search_info['manager_name'] +"%"

        if search_info['manager_phone']:
            params['manager_phone'] = "%" + search_info['manager_phone'] +"%"

        if search_info['manager_email']:
            params['manager_email'] = "%" + search_info['manager_email'] +"%"

        if search_info['start_date']:
            params['start_date'] = search_info['start_date']

        if search_info['end_date']:
            params['end_date'] = search_info['end_date']

        order = search_info['order']
        # sql실행시킬 시 예약어로 인식을 하지 못하는 에러 때문에 미리 변수에 넣어서 sql문자열에 합쳐준다.

        where_sql = ""

        if params['id']:
            where_sql += """
                AND
                    s.id = %(id)s
                """

        if params['seller_account']:
            where_sql += """
                AND
                    i.seller_account like %(seller_account)s
                """
        
        if params['english_name']:
            where_sql += """
                AND i.english_name like %(english_name)s
            """

        if params['korean_name']:
            where_sql += """
                AND 
                    i.korean_name like %(korean_name)s
            """

        if params['manager_name']:
            where_sql +=  """
                AND
                    m.name like %(manager_name)s
            """
        
        if params['seller_status']:
            where_sql += """
                AND 
                    t.name like %(seller_status)s
            """

        if params['manager_phone']:
            where_sql += """
                AND 
                    phone_number like %(manager_phone)s
                """

        if params['manager_email']:
            where_sql += """
                AND 
                    t.name like %(manager_email)s
                """

        if params['seller_property']:
            where_sql += """
                AND
                    p.name like %(seller_property)s
                """

        if params['start_date']  and params['end_date']:
            where_sql += """
                AND
                    s.register_date BETWEEN %(start_date)s and %(end_date)s
                """

        sql = """
            SELECT
                s.id as id, 
                i.seller_account as seller_account,
                i.cs_phone as cs_phone,
                i.english_name as english_name,
                i.korean_name as korean_name,
                m.name as manager_name,
                t.name as seller_status,
                m.phone_number as manager_phone_number,
                m.email as manager_email,
                p.name as seller_property,
                i.registered_product_count as registered_product_count,
                DATE_FORMAT(s.register_date,%(register_date)s) as register_date

            FROM sellers s

            INNER JOIN seller_informations i ON s.id = i.seller_id
            INNER JOIN seller_properties p ON i.seller_property_id = p.id
            INNER JOIN seller_statuses t ON i.seller_status_id = t.id
            INNER JOIN seller_managers m ON s.id = m.seller_id

            WHERE s.is_deleted = 0
            AND i.expired_at = '9999-12-31 23:59:59'
                """ + where_sql + """
            ORDER BY s.id """ + order + """;
        """

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
                ))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError('DATABASE IS NOT FOUND SELLER LIST')

        return results