# 작성자: 김태수
# 작성일: 2020.09.23.수
# Order에 관련된 로직을 처리하는 class
class OrderService:
    def __init__(self, order_dao, config):
        self.order_dao = order_dao
        self.config = config

    # 작성자: 김태수
    # 작성일: 2020.09.23.수
    # 주문 정보를 처리하는 로직
    def get_order_informations(self, status_name, offset, limit):
        try:
            order_data = self.order_dao.get_orders_and_order_details(status_name)[offset:limit]
            result = []
            for order_datum in order_data:
                option_id = order_datum['option_id']
                order_number = order_datum['order_number']
                order_detail_number = order_datum['order_detail_number']
                payment_price = order_datum['final_price']
                quantity = order_datum['quantity']
                order_status_id = order_datum['order_detail_statuses_id']
                order_detail_id = order_datum['id']
                order_id = order_datum['orders.id']
                payment_date = self.order_dao.get_payment_date(order_detail_id)['updated_at']
                option_information = self.order_dao.get_option_information(option_id)
                color_name = self.order_dao.get_color(option_information['color_id'])['name']
                size_name = self.order_dao.get_size(option_information['size_id'])['name']
                product_information = self.order_dao.get_product_information(option_information['product_id'])
                product_name = product_information['name']
                seller_name = self.order_dao.get_seller(product_information['seller_id'])['korean_name']
                option_name = color_name + "/" + size_name
                user_information = self.order_dao.get_user(order_datum['user_id'])
                user_name = user_information['last_name'] + user_information['first_name']
                phone_number = self.order_dao.get_shipping_information(order_datum['shipping_information_id'])['phone_number']

                row = {
                    'payment_date':payment_date,
                    'order_number':order_number,
                    'order_detail_number':order_detail_number,
                    'seller_name':seller_name,
                    'product_name':product_name,
                    'option_information':option_name,
                    'quantity':quantity,
                    'user_name':user_name,
                    'phone_number':phone_number,
                    'payment_price':payment_price,
                    'coupon_discount':0,
                    'order_status':status_name
                }

                result.append(row)

        except:
            raise
        else:
            return result

    def update_order_status(self, order_detail_numbers, update_status_name):
        try:
            for order_detail_number in order_detail_numbers:
                order_detail_id = self.order_dao.get_order_detail(order_detail_number)['id']
                self.order_dao.update_order_status(order_detail_id, update_status_name)
        except:
            raise
        else:
            return
