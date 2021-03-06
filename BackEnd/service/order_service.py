from datetime import datetime
class OrderService:
    def __init__(self, order_dao, config):
        self.order_dao = order_dao
        self.config    = config

    def get_order_data(self, db, arguments):
        """
        주문정보 - Business Layer(service) function
        Args:
            arguments = {
                'start_date'          : 조회 시작일,
                'end_date'            : 조회 종료일,
                'status_id'           : 주문 상태 아이디,
                'order_number'        : 주문 번호(검색),
                'detail_number'       : 주문 상세 번호(검색),
                'user_name'           : 주문자명(검색),
                'phone_number'        : 핸드폰번호(검색),
                'seller_name'         : 셀러명(검색),
                'product_name'        : 상품명(검색),
                'seller_properties'   : 셀러속성(검색),
                'offset'              : 페이지네이션 시작지점,
                'limit'               : 전달할 주문 리스트 개수
                'order_cancel_reason' : 주문 취소 사유,
                'order_refund_reason' : 환불 요청 사유
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
                "user_name"           : 주문자명,
                "current_updated_at"  : 현재 상태 변경일자
            }]
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
            2020-09-29 : 결제 일자 기준이 아닌 현재 상태 기준으로 조회하도록 변경
        """

        order_data = self.order_dao.get_order_data(db, arguments)
        count      = self.order_dao.get_order_data_count(db, arguments)['count']

        # 날짜 형식 맞춰주기 위한 반복문
        for order_datum in order_data:
            # 배송시작일이 필요한 경우
            if arguments['status_id'] == 7:
                order_datum['shipping_started_at'] = self.order_dao.get_status_date(db, {
                        'order_detail_id': order_datum['id'],
                        'status_id'      : 3
                    })['updated_at'].strftime('%Y-%m-%d %H:%M:%S')

            order_datum['payment_complete'] = self.order_dao.get_status_date(db, {
                'order_detail_id' : order_datum['id'],
                'status_id'       : 1
                })['updated_at'].strftime('%Y-%m-%d %H:%M:%S')

            order_datum['current_updated_at'] = order_datum['current_updated_at'].strftime('%Y-%m-%d %H:%M:%S')

        result = {
            'count'      : count,
            'order_data' : order_data
        }

        return result

    def update_order_status(self, db, arguments):
        """
        주문 상태 변경 - Business Layer(service) function
        Args:
            arguments = {
                'order_detail_id'     : 주문 상세 아이디,
                'to_status'           : 변경하고자 하는 주문상태 아이디,
                'order_cancel_reason' : 주문 취소 사유,
                'order_refund_reason' : 주문 환불 사유
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
            2020-10-04 : 환불 요청 취소 반영
        """

        # 환불 요청 취소일 경우는 이전 상태를 조회해서 변경하기 위한 조건문
        if arguments['to_status'] == 0:
            for order_detail_id in arguments['order_detail_id']:
                argument = {
                    'order_detail_id'        : [order_detail_id],
                    'to_status'              : self.order_dao.get_order_current_status(db, {'order_detail_id':order_detail_id})['order_status_id'],
                    'order_refund_reason_id' : None,
                    'order_cancel_reason_id' : None
                }
                self.order_dao.update_order_status(db, argument)
                self.order_dao.insert_order_status_history(db, argument)

            return ''

        arguments['order_cancel_reason_id'] = None
        arguments['order_refund_reason_id'] = None

        if arguments['order_cancel_reason']:
            arguments['order_cancel_reason_id'] = self.order_dao.get_cancel_reason_id(db, {"order_cancel_reason":arguments['order_cancel_reason']})['id']
            arguments['order_refund_reason_id'] = None

        elif arguments['order_refund_reason']:
            arguments['order_refund_reason_id'] = self.order_dao.get_refund_reason_id(db, {"order_refund_reason":arguments['order_refund_reason']})['id']
            arguments['order_cancel_reason_id'] = None

        self.order_dao.update_order_status(db, arguments)

        for order_detail_id in arguments['order_detail_id']:
            argument = {
                'order_detail_id' : order_detail_id,
                'to_status'       : arguments['to_status']
            }
            self.order_dao.insert_order_status_history(db, argument)

        return ''

    def get_order_detail(self, db, arguments):
        """
        주문 상세 페이지 정보 - Business Layer(service) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디
            }
            db = DATABASE Connection Instance
        Returns :
            order_detail_data = {
                "address"              : 주소,
                "discount_rate"        : 할인율,
                "final_price"          : 결제금액,
                "option_info"          : 옵션정보,
                "order_date"           : 주문일시,
                "order_detail_number"  : 주문상세번호,
                "order_number"         : 주문번호,
                "order_status_history" : [
                    {
                        "date"         : 날짜,
                        "order_status" : 주문상태
                    }
                ],
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
            2020-09-29 : 초기 생성
        """

        order_detail_data = self.order_dao.get_order_detail_data(db, arguments)

        order_detail_data['payment_complete'] = order_detail_data['payment_complete'].strftime('%Y-%m-%d %H:%M:%S')
        order_detail_data['order_date']       = order_detail_data['order_date'].strftime('%Y-%m-%d %H:%M:%S')

        order_status_history = self.order_dao.get_order_status_history(db, arguments)

        for status in order_status_history:
            status['date'] = status['date'].strftime('%Y-%m-%d %H:%M:%S')

        order_detail_data.update({'order_status_history' : order_status_history})

        return order_detail_data

    def put_address(self, db, arguments):
        """
        배송지 정보 수정 - Business layer(service) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디,
                'address'         : 배송지 주소,
                'detail_address'  : 배송지 상세 주소,
                'zip_code'        : 우편번호
            }
            db = DATABASE Connection Instance
        Returns :
            ''
        Author :
            김태수
        History:
            2020-10-04 : 초기 생성
        """

        self.order_dao.put_address(db, arguments)

        return ''
