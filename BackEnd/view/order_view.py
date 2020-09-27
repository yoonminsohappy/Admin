from flask import jsonify, request
from flask.views import MethodView

from datetime import date, timedelta

import config, connection, ast

class GetOrderDataView(MethodView):
    def __init__(self, service):
        self.service = service

    """
        주문정보리스트  - Presentation Layer(view) function
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
        Returns :
            KEY_ERROR, 400

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
    def get(self):
        try:
            db = connection.get_connection(config.database)

            start_date        = request.headers.get('start_date', None)
            end_date          = request.headers.get('end_date', None)
            seller_properties = ast.literal_eval(request.headers.get('seller_properties', None))
            status_name       = request.args.get('status', None)
            offset            = int(request.args.get('offset', -1))
            limit             = int(request.args.get('limit', -1))
            order_number      = "%" + request.args.get('order_number', "") + "%"
            detail_number     = "%" + request.args.get('detail_number', "") + "%"
            user_name         = "%" + request.args.get('user_name', "") + "%"
            phone_number      = "%" + request.args.get('phone_number', "") + "%"
            seller_name       = "%" + request.args.get('seller_name', "") + "%"
            product_name      = "%" + request.args.get('product_name', "") + "%"

            day      = timedelta(days = 1)
            end_date = date.fromisoformat(end_date) + day

            arguments = {
                'start_date'        : start_date,
                'end_date'          : end_date,
                'status_name'       : status_name,
                'order_number'      : order_number,
                'detail_number'     : detail_number,
                'user_name'         : user_name,
                'phone_number'      : phone_number,
                'seller_name'       : seller_name,
                'product_name'      : product_name,
                'seller_pro뷰perties' : seller_properties,
                'offset'            : offset,
                'limit'             : limit
            }

            order_data = self.service.get_order_data(db, arguments)

            if (not status_name) or (not start_date) or (not end_date) or (offset == -1) or (limit == -1):
                return jsonify({'message':'KEY_ERROR'}), 400

        except:
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            return jsonify(order_data), 200

        finally:
            db.close()

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

            SUCCESS, 200
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
    """
class PutOrderStatusView(MethodView):
    def __init__(self, service):
        self.service = service

    def put(self):
        try:
            db = connection.get_connection(config.database)
            data = request.get_json()
            order_detail_id = ast.literal_eval(data['order_detail_id'])
            to_status = data['to_status']
            arguments = {
                'order_detail_id' : order_detail_id,
                'to_status'       : to_status
            }

            self.service.update_order_status(db, arguments)

        except KeyError:
            db.rollback()
            return jsonify({'message':'KEY_ERROR'}), 400

        except:
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()

# 작성자: 김태수
# 작성일: 2020.09.27.일
# 주문 상태를 업데이트하는 뷰: 
class PutOrderStatusView(MethodView):
    def __init__(self, service):
        self.service = service

    def put(self):
        try:
            db = connection.get_connection(config.database)
            data = request.get_json()
            order_detail_id = ast.literal_eval(data['order_detail_id'])
            to_status = data['to_status']
            arguments = {
                'order_detail_id':order_detail_id,
                'to_status':to_status
            }

            self.service.update_order_status(db, arguments)

        except KeyError:
            db.rollback()
            return jsonify({'message':'KEY_ERROR'}), 400

        except:
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()
