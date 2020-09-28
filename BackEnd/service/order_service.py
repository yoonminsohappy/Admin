from datetime import datetime
class OrderService:
    def __init__(self, order_dao, config):
        self.order_dao = order_dao
        self.config = config

    """
        주문정보 - Business Layer(service) function
        Args:
            arguments = {
                'start_date'        : 조회 시작일,
                'end_date'          : 조회 종료일,
                'status_name'       : 주문 상태명,
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
            status_name            = {'status_name':arguments['status_name']}
            arguments['status_id'] = self.order_dao.get_order_status_id(db, status_name)['id']
            order_data  = self.order_dao.get_order_data(db, arguments)

            for order_datum in order_data:
                if arguments['status_id'] != 1 and arguments['status_id'] != 2:
                    args = {
                        'order_detail_id' : order_datum['id'],
                        'status_id'       : arguments['status_id']
                    }
                    order_datum['current_updated_at'] = self.order_dao.get_current_status_date(db, args)['updated_at'].strftime('%Y-%m-%d %H:%M:%S')

                order_datum['payment_complete']   = order_datum['payment_complete'].strftime('%Y-%m-%d %H:%M:%S')

        except:
            raise
        else:
            return order_data

    """
        주문 상태 변경 - Business Layer(service) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디,
                'to_status'       : 변경하고자 하는 주문상태명
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
