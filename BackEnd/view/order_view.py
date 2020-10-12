from flask import jsonify, request
from flask.views import MethodView

from datetime import date, timedelta
from pymysql  import err

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
                "current_updated_at"  : 현재 상태 업데이트 일자,
                "order_cancel_reason" : 주문 취소 사유,
                "order_refund_reason" : 환불 요청 사유
            }], 200
        Author :
            김태수
        History:
            2020-09-28 : 초기 생성
        """

        try:
            db = connection.get_connection()

            start_date          = request.args.get('start_date', None)
            end_date            = request.args.get('end_date', None)
            seller_properties   = ast.literal_eval(request.args.get('seller_properties', None))
            status_id           = request.args.get('status_id', None)
            offset              = int(request.args.get('offset', -1))
            limit               = offset + int(request.args.get('limit', -1))
            order_cancel_reason = request.args.get('order_cancel_reason', None)
            order_refund_reason = request.args.get('order_refund_reason', None)
            order_number        = "%" + request.args.get('order_number', "") + "%"
            detail_number       = "%" + request.args.get('detail_number', "") + "%"
            user_name           = "%" + request.args.get('user_name', "") + "%"
            phone_number        = "%" + request.args.get('phone_number', "") + "%"
            seller_name         = "%" + request.args.get('seller_name', "") + "%"
            product_name        = "%" + request.args.get('product_name', "") + "%"

            # seller_properties가 여러 개의 값이 아닌 하나로 들어올 경우
            # int형으로 오는 것을 tuple로 변환
            if isinstance(seller_properties, int):
                seller_properties = [seller_properties]

            # 필수로 들어와야할 Key가 들어오지 않았을 경우 KEY_ERROR 반환
            if (not status_id) or (offset == -1) or (limit == -1):
                return jsonify({'message':'KEY_ERROR'}), 400

            # start_date가 들어오지 않았을 경우 가장 앞선 날짜로 설정
            if not start_date:
                start_date = str(date.min)

            # end_date가 들어오지 않았을 경우 오늘 날짜로 설정
            if not end_date:
                end_date = str(date.today())

            # 날짜만 들어와서 00시를 기준으로 비교하게 되기에
            # 하루를 더해서 마지막 날짜로 들어온 값도 포함되도록 설정
            day      = timedelta(days = 1)
            end_date = str(date.fromisoformat(end_date) + day)

            # start_date가 end_date보다 뒤의 날짜일 경우 INVALID_DATE 반환
            if start_date > end_date:
                return jsonify({'message':'INVALID_DATE'}), 400

            arguments = {
                'start_date'          : start_date,
                'end_date'            : end_date,
                'status_id'           : status_id,
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

        except err.OperationalError:
            return jsonify({'message':'DB_DISCONNECTED'}), 500

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
            db = connection.get_connection()
            data = request.get_json()

            arguments = {
                'order_detail_id'     : ast.literal_eval(data['order_detail_id']),
                'to_status'           : data['to_status'],
                'order_cancel_reason' : None,
                'order_refund_reason' : None
            }

            if data['to_status'] == 6:
                arguments['order_cancel_reason'] = data['order_cancel_reason']
                arguments['order_refund_reason'] = None
            elif data['to_status'] == 7:
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

        except err.OperationalError:
            return jsonify({'message':'DB_DISCONNECTED'}), 500

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
            db = connection.get_connection()

            order_detail_id = request.args.get('order_detail_id', None)

            if not order_detail_id:
                return jsonify({'message':'KEY_ERROR'}), 400

            arguments = {
                'order_detail_id':order_detail_id
            }

            order_detail_data = self.service.get_order_detail(db, arguments)

        except ValueError:
            return jsonify({'message':'VALUE_ERROR'}), 400

        except err.OperationalError:
            return jsonify({'message':'DB_DISCONNECTED'}), 500

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
        """
        배송지 정보 수정 - Presentation Layer(view) function
        Args:
            arguments = {
                'order_detail_id' : 주문 상세 아이디,
                'address'         : 배송지 주소,
                'detail_address'  : 배송지 상세 주소,
                'zip_code'        : 우편번호
            }
        Returns :
            KEY_ERROR, 400
            UNSUCCESS, 400
            SUCCESS, 200
        Author :
            김태수
        History:
            2020-10-04 : 초기 생성
        """

        try:
            db = connection.get_connection()

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

        except ValueError:
            db.rollback()
            return jsonify({'message':'VALUE_ERROR'}), 400

        except err.OperationalError:
            return jsonify({'message':'DB_DISCONNECTED'}), 500

        except:
            traceback.print_exc()
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400

        else:
            db.commit()
            return jsonify({'message':'SUCCESS'}), 200

        finally:
            db.close()
