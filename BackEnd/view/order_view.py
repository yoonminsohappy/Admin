from flask import jsonify, request
from flask.views import MethodView

from datetime import date, timedelta

import config, connection, ast

import traceback

class GetOrderDataView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        주문정보리스트  - Presentation Layer(view) function
        Args:
            arguments = {
                'start_date'          : 조회 시작일,
                'end_date'            : 조회 종료일,
                'status_name'         : 주문 상태명,
                'order_number'        : 주문 번호(검색),
                'detail_number'       : 주문 상세 번호(검색),
                'user_name'           : 주문자명(검색),
                'phone_number'        : 핸드폰번호(검색),
                'seller_name'         : 셀러명(검색),
                'product_name'        : 상품명(검색),
                'seller_properties'   : 셀러속성(검색),
                'offset'              : 페이지네이션 시작지점,
                'limit'               : 전달할 주문 리스트 개수,
                'order_cancel_reason' : 주문 취소 사유(검색),
                'order_refund_reason' : 환불 요청 사유(검색)
            }
        Returns :
            KEY_ERROR, 400
            VALUE_ERROR, 400
            order_data = [{
                "final_price"         : 결제금액
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
                "current_updated_at"  : 현재 상태 업데이트 일자
            }]
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
        """
        try:
            db = connection.get_connection(config.database)

            start_date          = request.headers.get('start_date', None)
            end_date            = request.headers.get('end_date', None)
            seller_properties   = ast.literal_eval(request.headers.get('seller_properties', None))
            status_name         = request.args.get('status', None)
            offset              = int(request.args.get('offset', -1))
            limit               = int(request.args.get('limit', -1))
            order_cancel_reason = request.args.get('order_cancel_reason', None)
            order_refund_reason = request.args.get('order_refund_reason', None)
            order_number        = "%" + request.args.get('order_number', "") + "%"
            detail_number       = "%" + request.args.get('detail_number', "") + "%"
            user_name           = "%" + request.args.get('user_name', "") + "%"
            phone_number        = "%" + request.args.get('phone_number', "") + "%"
            seller_name         = "%" + request.args.get('seller_name', "") + "%"
            product_name        = "%" + request.args.get('product_name', "") + "%"

            if (not status_name) or (not start_date) or (offset == -1) or (limit == -1):
                return jsonify({'message':'KEY_ERROR'}), 400

            if end_date == None:
                end_date = str(date.today())

            day      = timedelta(days = 1)
            end_date = str(date.fromisoformat(end_date) + day)

            arguments = {
                'start_date'          : start_date,
                'end_date'            : end_date,
                'status_name'         : status_name,
                'order_number'        : order_number,
                'detail_number'       : detail_number,
                'user_name'           : user_name,
                'phone_number'        : phone_number,
                'seller_name'         : seller_name,
                'product_name'        : product_name,
                'seller_properties'   : seller_properties,
                'offset'              : offset,
                'limit'               : limit,
                'order_cancel_reason' : order_cancel_reason,
                'order_refund_reason' : order_refund_reason
            }

            order_data = self.service.get_order_data(db, arguments)

        except ValueError:
            traceback.print_exc()
            return jsonify({'message':'VALUE_ERROR'}), 400

        except:
            traceback.print_exc()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            return jsonify(order_data), 200

        finally:
            db.close()

class PutOrderStatusView(MethodView):
    def __init__(self, service):
        self.service = service

    def put(self):
        """
        주문 상태 변경 - Presentation Layer(view) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디,
                'to_status'       : 변경하고자 하는 주문상태명
            }
            db = DATABASE Connection Instance
        Returns :
            KEY_ERROR, 400
            VALUE_ERROR, 400
            SUCCESS, 200
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
        """
        try:
            db = connection.get_connection(config.database)
            data = request.get_json()

            arguments = {
                'order_detail_id' : ast.literal_eval(data['order_detail_id']),
                'to_status'       : data['to_status'],
                'order_cancel_reason' : None,
                'order_refund_reason' : None
            }

            if data['to_status'] == '주문취소완료':
                arguments['order_cancel_reason'] = data['order_cancel_reason']
                arguments['order_refund_reason'] = None
            elif data['to_status'] == '환불요청':
                arguments['order_refund_reason'] = data['order_refund_reason']
                arguments['order_cancel_reason'] = None

            self.service.update_order_status(db, arguments)

        except KeyError:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'KEY_ERROR'}), 400

        except ValueError:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'VALUE_ERROR'}), 400

        except:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()

class GetOrderDetailDataView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        주문 상세 페이지 정보 - Presentation Layer(view) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디
            }
        Returns :
            KEY_ERROR, 400
            VALUE_ERROR, 400
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
        try:
            db = connection.get_connection(config.database)

            order_detail_id = request.args.get('order_detail_id', None)

            if not order_detail_id:
                return jsonify({'message':'KEY_ERROR'}), 400

            arguments = {
                'order_detail_id':order_detail_id
            }

            order_detail_data = self.service.get_order_detail(db, arguments)

        except ValueError:
            return jsonify({'message':'VALUE_ERROR'}), 400

        except:
            traceback.print_exc()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            return jsonify(order_detail_data), 200
        finally:
            db.close()

class PutAddress(MethodView):
    def __init__(self, service):
        self.service = service

    def put(self):
        try:
            db = connection.get_connection(config.database)

            data = request.get_json()

            arguments = {
                'order_detail_id' : data['order_detail_id'],
                'address'         : data['address'],
                'detail_address'  : data['detail_address'],
                'zip_code'        : data['zip_code']
            }

            self.service.put_address(db, arguments)

        except KeyError:
            db.rollback()
            return jsonify({'message':'KEY_ERROR'}), 400

        except:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()
