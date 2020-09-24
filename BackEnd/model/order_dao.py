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
                osmh.updated_at >= %s
                AND osmh.updated_at <= %s
                AND d.order_detail_statuses_id = (SELECT id FROM order_statuses WHERE name = %s)
                AND o.order_number LIKE %s
                AND d.order_detail_number LIKE %s
                AND u.name LIKE %s
                AND s.phone_number LIKE %s
                AND sl.korean_name LIKE %s
                AND pd.name LIKE %s
                AND sl.seller_property_id IN %s
            LIMIT %s, %s;
            """
            cursor.execute(sql, arguments)
            payment = cursor.fetchall()
        except:
            raise
        else:
            return payment
        finally:
            cursor.close()
