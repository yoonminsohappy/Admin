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
    # 주문 정보를 처리하는 서비스
    def get_order_informations(self, db, arguments):
        try:
            status_name            = {'status_name':arguments['status_name']}
            arguments['status_id'] = self.order_dao.get_order_status_id(db, status_name)['id']
            payment_complete_data  = self.order_dao.get_payment_complete_order_data(db, arguments)

            for payment_complete_datum in payment_complete_data:
                payment_complete_datum['updated_at'] = payment_complete_datum['updated_at'].strftime('%Y-%m-%d %H:%M:%S')

        except:
            raise
        else:
            return payment_complete_data

    # 작성자: 김태수
    # 작성일: 2020.09.27.일
    # 주문상태를 업데이트하는 서비스
    def update_order_status(self, db, arguments):
        try:
            status_name            = {'status_name':arguments['to_status']}
            arguments['status_id'] = self.order_dao.get_order_status_id(db, status_name)['id']

            self.order_dao.update_order_status(db, arguments)

            for order_detail_id in arguments['order_detail_id']:
                argument = {
                    'order_detail_id' : order_detail_id,
                    'status_id'       : arguments['status_id']
                }
                self.order_dao.insert_order_status_history(db, argument)

        except:
            raise
        else:
            return ''
