import pymysql
from connection import get_connection

class OrderDao:
    def get_order_data(self, db, arguments):
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
                "current_updated_at"  : 결제완료 일시,
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
            2020-09-29 : 결제 일자 기준이 아닌 현재 상태 기준으로 조회하도록 변경
        """
        sql_1 = """
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
            osmh.updated_at AS current_updated_at,
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
            AND sl.seller_property_id IN %(seller_properties)s
            AND osmh.order_status_id = %(status_id)s
        """
        sql_2 = """
        ORDER BY osmh.updated_at DESC
        LIMIT %(offset)s, %(limit)s;
        """

        if arguments['order_number'] != "%"+"%":
            sql_1 += "AND o.order_number LIKE " + "%(order_number)s"
        elif arguments['detail_number'] != "%"+"%":
            sql_1 += "AND d.order_detail_number LIKE " + "%(detail_number)s"
        elif arguments['user_name'] != "%"+"%":
            sql_1 += "AND u.name LIKE " + "%(user_name)s"
        elif arguments['phone_number'] != "%"+"%":
            sql_1 += "AND s.phone_number LIKE " + "%(phone_number)s"
        elif arguments['seller_name'] != "%"+"%":
            sql_1 += "AND sl.korean_name LIKE " + "%(seller_name)s"
        elif arguments['product_name'] != "%"+"%":
            sql_1 += "AND pd.name LIKE " + "%(product_name)s"

        sql = sql_1 + sql_2

        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            order_data = cursor.fetchall()

        return order_data

    def get_payment_complete_status_date(self, db, argument):
        """
         결제일자 정보 - Persistence Layer(model) function
        Args:
            arguments = {
                "order_detail_id" : 주문 상세 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            {current_status_date : 현재 상태 업데이트 일자}
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
            2020-09-29 : 현재 상태 업데이트 일자 > 결제일자
        """
        sql = """
        SELECT
            updated_at AS payment_complete
        FROM
            order_status_modification_histories
        WHERE
            order_detail_id = %(order_detail_id)s
            AND order_status_id = 1;
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, argument)
            payment_complete = cursor.fetchone()

        if not payment_complete:
            raise ValueError

        return payment_complete

    def get_order_status_id(self, db, argument):
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
        sql = """
        SELECT
            id
        FROM
            order_statuses
        WHERE
            name = %(status_name)s;
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, argument)
            status_id = cursor.fetchone()

        if not status_id:
            raise ValueError

        return status_id

    def update_order_status(self, db, arguments):
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
        sql = """
        UPDATE
            order_details
        SET
            order_detail_statuses_id = %(status_id)s
        WHERE
            id IN %(order_detail_id)s;
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, arguments)

        if not result:
            raise

        return ''

    def insert_order_status_history(self, db, argument):
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
        sql = """
        INSERT INTO
            order_status_modification_histories
        (order_detail_id, updated_at, order_status_id)
            VALUES
        (%(order_detail_id)s, NOW(), %(status_id)s);
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, argument)

        if not result:
            raise

        return ''

    def get_order_detail_data(self, db, arguments):
        """
        주문 상세 페이지 정보 - Persistence Layer(model) function
        Args:
            arguments = {
                'order_detail_id' : 주문상세번호
            }
            db = DATABASE Connection Instance
        Returns :
            order_detail_data = {
                "address"               : 주소,
                "discount_rate"         : 할인율,
                "final_price"           : 결제금액,
                "option_info"           : 옵션정보,
                "order_date"            : 주문일시,
                "order_detail_number"   : 주문상세번호,
                "order_number"          : 주문번호,
                "payment_complete"      : 결제일시,
                "product_id"            : 상품번호,
                "product_name"          : 상품명,
                "quantity"              : 수량,
                "receiver"              : 수취인,
                "receiver_phone_number" : 수취인 휴대폰번호,
                "sale_price"            : 상품가격,
                "seller_name"           : 브랜드명,
                "shipping_memo"         : 배송메모,
                "user_id"               : 회원번호,
                "user_name"             : 주문자명,
                "user_phone_number"     : 주문자휴대폰번호
            }
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
        """
        sql = """
        SELECT
            d.order_detail_number AS order_detail_number,
            o.order_number AS order_number,
            o.order_date AS order_date,
            o.final_price AS final_price,
            osmh.updated_at AS payment_complete,
            u.phone_number AS user_phone_number,
            p.id AS product_id,
            pd.name AS product_name,
            pd.sale_price AS sale_price,
            pd.discount_rate AS discount_rate,
            sl.korean_name AS seller_name,
            CONCAT(c.name, "/", z.name) AS option_info,
            d.quantity AS quantity,
            u.id AS user_id,
            u.name AS user_name,
            si.name AS receiver,
            si.phone_number AS receiver_phone_number,
            si.address AS address,
            si.shipping_memo AS shipping_memo
        FROM
            order_details d
        LEFT JOIN orders o
            ON o.id = d.order_id
        LEFT JOIN order_status_modification_histories osmh
            ON d.id = osmh.order_detail_id
        LEFT JOIN users u
            ON o.user_id = u.id
        LEFT JOIN options op
            ON op.id = d.option_id
        LEFT JOIN colors c
            ON c.id = op.color_id
        LEFT JOIN sizes z
            ON z.id = op.size_id
        LEFT JOIN products p
            ON p.id = op.product_id
        LEFT JOIN product_details pd
            ON pd.product_id = op.product_id
        LEFT JOIN sellers sl
            ON sl.id = p.seller_id
        LEFT JOIN shipping_informations si
            ON si.id = o.shipping_information_id
        WHERE
            d.id = %(order_detail_id)s
        AND osmh.order_status_id = 1
        AND osmh.order_detail_id = %(order_detail_id)s;
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            order_detail_data = cursor.fetchone()

        if not order_detail_data:
            raise ValueError

        return order_detail_data

    def get_order_status_history(self, db, arguments):
        """
        주문 상태 변경 내역 - Persistence Layer(model) function
        Args:
            arguments = {
                'order_detail_id' : 주문상세번호
            }
            db = DATABASE Connection Instance
        Returns :
            "order_status_history" = [
                {
                    "date"         : 날짜,
                    "order_status" : 주문상태
                }
            ]
        Author :
            김태수
        History:
            2020-09-29 : 초기 생성
        """
        sql = """
        SELECT
            osmh.updated_at AS date,
            os.name AS order_status
        FROM
            order_status_modification_histories osmh
        LEFT JOIN order_statuses os
            ON os.id = osmh.order_status_id
        WHERE
            osmh.order_detail_id = %(order_detail_id)s;
        """
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, arguments)
            order_status_history = cursor.fetchall()

        if not order_status_history:
            raise ValueError

        return order_status_history
