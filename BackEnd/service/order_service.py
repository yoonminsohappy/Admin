from datetime import datetime
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
    def get_order_informations(self, db, arguments):
        try:
            payment_complete_data = self.order_dao.get_payment_complete_order_data(db, arguments)

            for payment_complete_datum in payment_complete_data:
                payment_complete_datum['updated_at'] = payment_complete_datum['updated_at'].strftime('%Y-%m-%d %H:%M:%S')

        except:
            raise
        else:
            return payment_complete_data
