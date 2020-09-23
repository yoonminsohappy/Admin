import pymysql
from flask import jsonify, request
from connection import get_connection

# 작성자: 김태수
# 작성일: 2020.09.22.화
# order와 연결된 Class
class OrderDao:
    def __init__(self, db):
        self.db = db

    # 작성자: 김태수
    # 작성일: 2020.09.22.화
    # 주문정보를 데이터베이스에서 가져오는 함수
    def get_orders_and_order_details(self, status_name):
        try:
            db     = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM order_details
            LEFT JOIN orders
            ON order_details.order_id = orders.id
            WHERE (
            SELECT id
            FROM order_statuses
            WHERE name = %s
            ) = order_details.order_detail_statuses_id;
            """

            cursor.execute(sql, status_name)
            order_data = cursor.fetchall()

        except:
            raise
        else:
            return order_data if order_data else None
        finally:
            cursor.close()
            db.close()

    def get_payment_date(self, order_detail_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT updated_at
            FROM order_status_modification_histories
            WHERE order_detail_id = %s;
            """

            cursor.execute(sql, order_detail_id)
            payment_date = cursor.fetchone()

        except:
            raise
        else:
            return payment_date if payment_date else None
        finally:
            cursor.close()
            db.close()


    def get_option_information(self, option_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM options
            WHERE id = %s;
            """

            cursor.execute(sql, option_id)
            option_information = cursor.fetchone()

        except:
            raise
        else:
            return option_information if option_information else None
        finally:
            cursor.close()
            db.close()

    def get_color(self, color_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM colors
            WHERE id = %s
            """

            cursor.execute(sql, color_id)
            color = cursor.fetchone()

        except:
            raise
        else:
            return color if color else None
        finally:
            cursor.close()
            db.close()

    def get_size(self, size_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM sizes
            WHERE id = %s
            """

            cursor.execute(sql, size_id)
            size = cursor.fetchone()

        except:
            raise
        else:
            return size if size else None
        finally:
            cursor.close()
            db.close()

    def get_product_information(self, product_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM products
            LEFT JOIN product_details
            ON product_details.product_id = products.id
            WHERE products.id = %s
            """

            cursor.execute(sql, product_id)
            product_information = cursor.fetchone()

        except:
            raise
        else:
            return product_information if product_information else None
        finally:
            cursor.close()
            db.close()

    def get_seller(self, seller_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM sellers
            WHERE id = %s
            """

            cursor.execute(sql, seller_id)
            seller = cursor.fetchone()

        except:
            raise
        else:
            return seller if seller else None
        finally:
            cursor.close()
            db.close()

    def get_shipping_information(self, shipping_information_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM shipping_informations
            WHERE id = %s
            """

            cursor.execute(sql, shipping_information_id)
            shipping_information = cursor.fetchone()

        except:
            raise
        else:
            return shipping_information if shipping_information else None
        finally:
            cursor.close()
            db.close()

    def get_user(self, user_id):
        try:
            db = get_connection(self.db)
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT *
            FROM users
            WHERE id = %s
            """

            cursor.execute(sql, user_id)
            user = cursor.fetchone()

        except:
            raise
        else:
            return user if user else None
        finally:
            cursor.close()
            db.close()
