import pymysql

from flask      import jsonify

class UserDao:
    def find_search_total_user_list(self, conn, search_info):
        """
        유저커뮤니티 전체 리스트, 검색 기능 API

        Args:
            conn        :   데이터베이스 커넥션 객체
            search_info :   검색 데이터를 담을 리스트

        Retruns:
            200, results : 해당 검색에 대한 결과
            400, {'message': 'UNSUCCESS'} : 검색실패시

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020.10.01(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경, register_date 날짜 형식 변경

        """
        params = dict()
        
        params = {
            'id':None, 
            'account_id':None, 
            'user_name':None,
            'user_phone':None,
            'user_email':None,
            'start_date':None,
            'end_date':None
        }

        if search_info['id']:
            params['id'] = "%" + search_info['id'] +"%"

        if search_info['account_id']:
            params['account_id'] = "%" + search_info['account_id'] +"%"

        if search_info['user_name']:
            params['user_name'] = "%" + search_info['user_name'] +"%"

        if search_info['user_phone']:
            params['user_phone'] = "%" + search_info['user_phone'] +"%"

        if search_info['user_email']:
            params['user_email'] = "%" + search_info['user_email'] +"%"

        if search_info['start_date']:
            params['start_date'] = search_info['start_date']

        if search_info['end_date']:
            params['end_date'] = search_info['end_date']

        where_sql = ""

        if params['id']:
            where_sql += """
                AND
                    u.id = %(id)s
                """

        if params['account_id']:
            where_sql += """
                AND
                    ui.account_id like %(account_id)s
                """

        if params['user_name']:
            where_sql += """
                AND
                    ui.name like %(user_name)s
                """

        if params['user_phone']:
            where_sql += """
                AND
                    ui.phone_number like %(user_phone)s
                """

        if params['user_email']:
            where_sql += """
                AND
                    ui.email like %(user_email)s
                """

        if params['start_date']  and params['end_date']:
            where_sql += """
                AND
                    u.register_date BETWEEN %(start_date)s and %(end_date)s
                """

        sql = """
            SELECT
            count(*) as count
            FROM users u
            INNER JOIN user_informations ui ON ui.user_id = u.id
            WHERE
                u.is_deleted = 0 
                """ + where_sql + """
        """
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
                ))
            results = cursor.fetchone()
            if not results:
                raise pymysql.err.InternalError('DATABASE IS NOT FOUND TOTAL_USER_COUNT')

        return results['count']

    def find_search_user_list(self, conn, search_info):
        
        params = dict()
        
        params = {
            'id':None, 
            'account_id':None, 
            'user_name':None,
            'user_phone':None,
            'user_email':None,
            'start_date':None,
            'end_date':None,
            'page':None,
            'per_page':None,
            'register_date':"%Y-%m-%d %H:%i:%s"
        }

        if search_info['id']:
            params['id'] = "%" + search_info['id'] +"%"

        if search_info['account_id']:
            params['account_id'] = "%" + search_info['account_id'] +"%"

        if search_info['user_name']:
            params['user_name'] = "%" + search_info['user_name'] +"%"

        if search_info['user_phone']:
            params['user_phone'] = "%" + search_info['user_phone'] +"%"

        if search_info['user_email']:
            params['user_email'] = "%" + search_info['user_email'] +"%"

        if search_info['start_date']:
            params['start_date'] = search_info['start_date']

        if search_info['end_date']:
            params['end_date'] = search_info['end_date']

        where_sql = ""

        if params['id']:
            where_sql += """
                AND
                    u.id = %(id)s
                """

        if params['account_id']:
            where_sql += """
                AND
                    ui.account_id like %(account_id)s
                """

        if params['user_name']:
            where_sql += """
                AND
                    ui.name like %(user_name)s
                """

        if params['user_phone']:
            where_sql += """
                AND
                    ui.phone_number like %(user_phone)s
                """

        if params['user_email']:
            where_sql += """
                AND
                    ui.email like %(user_email)s
                """

        if params['start_date']  and params['end_date']:
            where_sql += """
                AND
                    u.register_date BETWEEN %(start_date)s and %(end_date)s
                """

        params['page'] = (int(search_info['page'])-1)*10
        params['per_page'] = search_info['per_page']

        order = search_info['order']

        sql = """
            SELECT 
            u.id,
            ui.account_id,
            DATE_FORMAT(u.register_date,%(register_date)s) as register_date,
            ui.name,         
            ui.email,
            ui.phone_number
            FROM users u
            INNER JOIN user_informations ui ON ui.user_id = u.id
            WHERE u.is_deleted = 0
            """ + where_sql + """
            ORDER BY u.id """ + order + """
            LIMIT %(page)s, %(per_page)s;
        """
 
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, (
                params
                ))
            results = cursor.fetchall()
            if not results:
                raise pymysql.err.InternalError('DATABASE IS NOT FOUND USER_LIST')

        return results