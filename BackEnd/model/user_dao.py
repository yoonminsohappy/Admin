import pymysql

from flask      import jsonify

class UserDao:
    def find_search_total_user_list(self, conn, search_info):
        sql = """
            SELECT
            count(*) as count
            FROM users u
            INNER JOIN user_informations ui ON ui.user_id = u.id
            WHERE u.id like %s
                AND ui.account_id like %s
                AND ui.email like %s
                AND ui.phone_number like %s
            ORDER BY u.id DESC;
        """

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(sql, (
            "%" + search_info['id'] +"%",
            "%" + search_info['account_id'] + "%",
            "%" + search_info['user_email'] +"%",
            "%" + search_info['user_phone'] + "%"
        ))

        results = cursor.fetchone()['count']
        cursor.close()

        return results if results else None

    def find_search_user_list(self, conn, search_info):
        
        order = search_info['order']

        sql = """
            SELECT 
            u.id,
            ui.account_id,
            u.register_date,         
            ui.email,
            ui.phone_number
            FROM users u
            INNER JOIN user_informations ui ON ui.user_id = u.id
            WHERE u.id like %s
                AND ui.account_id like %s
                AND ui.email like %s
                AND ui.phone_number like %s
                AND u.is_deleted != 1
            ORDER BY u.id """ + order + """
            LIMIT %s, 10;
        """
 
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(sql, (
            "%" +   ['id'] +"%",
            "%" + search_info['account_id'] + "%",
            "%" + search_info['user_email'] +"%",
            "%" + search_info['user_phone'] + "%",
             (int(search_info['page'])-1)*10
            ))
        results = cursor.fetchall()

        cursor.close()

        return results if results else None