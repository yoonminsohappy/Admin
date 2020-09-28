import pymysql
from connection import get_connection

class OrderDao:
    """
        주문정보 - Persistence Layer(model) function
        Args:
            arguments = {
                'start_date'        : 조회 시작일,
                'end_date'          : 조회 종료일,
                'status_id'         : 주문 상태 아이디,
                'order_number'      : 주문 번호(검색),
                'detail_number'     : 주문 상세 번호(검색),
                'user_name'         : 주문자명(검색),
                'phone_number'      : 핸드폰번호(검색),
                'seller_name'       : 셀러명(검색),
                'product_name'      : 상품명(검색),
                'seller_properties' : 셀러속성(검색),
                'offset'            : 페이지네이션 시작지점,
                'limit'             : 전달할 주문 리스트 개수
            }
            db = DATABASE Connection Instance
        Returns :
            order_data = [{
                "final_price"         : 결제금액,
                "id"                  : 주문상세 아이디,
                "option_info"         : 옵션정보,
                "order_detail_number" : 주문상세번호,
                "order_number"        : 주문 번호,
                "payment_complete"    : 결제완료 일시,
                "phone_number"        : 핸드폰 번호,
                "product_name"        : 상품명,
                "quantity"            : 수량,
                "seller_name"         : 셀러명,
                "user_name"           : 주문자명
            }]
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
    def get_order_data(self, db, arguments):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT
                d.id AS id,
                o.order_number AS order_number,
                d.order_detail_number AS order_detail_number,
                o.final_price AS final_price,
                u.name AS user_name,
                d.quantity AS quantity,
                pd.name AS product_name,
                sl.korean_name AS seller_name,
                s.phone_number AS phone_number,
                osmh.updated_at AS payment_complete,
                CONCAT(c.name, "/", z.name) AS option_info
            FROM
                order_details d

                LEFT JOIN orders o
                    ON d.order_id = o.id
                LEFT JOIN users u
                    ON o.user_id = u.id
                LEFT JOIN shipping_informations s
                    ON s.id = o.shipping_information_id
                LEFT JOIN options i
                    ON d.option_id = i.id
                LEFT JOIN colors c
                    ON i.color_id = c.id
                LEFT JOIN sizes z
                    ON i.size_id = z.id
                LEFT JOIN products p
                    ON i.product_id = p.id
                LEFT JOIN product_details pd
                    ON pd.id = i.product_id
                LEFT JOIN sellers sl
                    ON sl.id = p.seller_id
                LEFT JOIN order_status_modification_histories osmh
                    ON osmh.order_detail_id = d.id
            WHERE
                osmh.updated_at >= %(start_date)s
                AND osmh.updated_at <= %(end_date)s
                AND d.order_detail_statuses_id = %(status_id)s
                AND o.order_number LIKE %(order_number)s
                AND d.order_detail_number LIKE %(detail_number)s
                AND u.name LIKE %(user_name)s
                AND s.phone_number LIKE %(phone_number)s
                AND sl.korean_name LIKE %(seller_name)s
                AND pd.name LIKE %(product_name)s
                AND sl.seller_property_id IN %(seller_properties)s
                AND osmh.order_status_id = 1
            ORDER BY osmh.updated_at DESC
            LIMIT %(offset)s, %(limit)s;
            """
            cursor.execute(sql, arguments)
            order_data = cursor.fetchall()

        except:
            raise
        else:
            return order_data
        finally:
            cursor.close()

    """
        주문 상태 업데이트 정보 - Persistence Layer(model) function
        Args:
            arguments = {
                "order_detail_id" : 주문 상세 아이디,
                "status_id"       : 현재 상태 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            {current_status_date : 현재 상태 업데이트 일자}
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
    def get_current_status_date(self, db, argument):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT
                updated_at
            FROM
                order_status_modification_histories
            WHERE
                order_detail_id = %(order_detail_id)s
                AND order_status_id = %(status_id)s
            """

            cursor.execute(sql, argument)
            current_status_date = cursor.fetchone()

        except :
            raise
        else:
            return current_status_date
        finally:
            cursor.close()

    """
        주문 상태 아이디 정보 - Persistence Layer(model) function
        Args:
            arguments = {
                "status_name" : 상태명,
            }
            db = DATABASE Connection Instance
        Returns :
            {status_id : 상태 아이디}
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
    def get_order_status_id(self, db, argument):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT
                id
            FROM
                order_statuses
            WHERE
                name = %(status_name)s;
            """

            cursor.execute(sql, argument)
            status_id = cursor.fetchone()

        except:
            raise
        else:
            return status_id
        finally:
            cursor.close()

    """
        주문 상태 업데이트 - Persistence Layer(model) function
        Args:
            arguments = {
                "status_id"       : 상태아이디,
                "order_detail_id" : 주문 상세 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
    def update_order_status(self, db, arguments):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            UPDATE
                order_details
            SET
                order_detail_statuses_id = %(status_id)s
            WHERE
                id IN %(order_detail_id)s;
            """

            cursor.execute(sql, arguments)

        except:
            raise
        else:
            return ''
        finally:
            cursor.close()

    """
        주문 상태 변경내역 업데이트 - Persistence Layer(model) function
        Args:
            arguments = {
                "status_id"       : 상태아이디,
                "order_detail_id" : 주문 상세 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
    def insert_order_status_history(self, db, argument):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            INSERT INTO
                order_status_modification_histories
            (order_detail_id, updated_at, order_status_id)
                VALUES
            (%(order_detail_id)s, NOW(), %(status_id)s);
            """

            cursor.execute(sql, argument)

        except:
            raise
        else:
            return ''
        finally:
            cursor.close()
