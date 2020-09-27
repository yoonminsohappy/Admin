import pymysql
from connection import get_connection

# 작성자: 김태수
# 작성일: 2020.09.23.수
# order와 연결된 Class
class OrderDao:
    # 작성자: 김태수
    # 작성일: 2020.09.23.수
    def get_payment_complete_order_data(self, db, arguments):
        try:
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT
                d.id,
                o.order_number,
                d.order_detail_number,
                o.final_price,
                u.name,
                c.name,
                z.name,
                d.quantity,
                pd.name,
                sl.korean_name,
                s.phone_number,
                osmh.updated_at
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
            ORDER BY osmh.updated_at DESC
            LIMIT %(offset)s, %(limit)s;
            """
            cursor.execute(sql, arguments)
            payment_order_data = cursor.fetchall()

        except:
            raise
        else:
            return payment_order_data
        finally:
            cursor.close()

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
