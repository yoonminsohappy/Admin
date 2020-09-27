from flask import jsonify, request
from flask.views import MethodView

from datetime import date, timedelta

import config, connection, ast

# 작성자: 김태수
# 작성일: 2020.09.17.목
class GetOrderDataView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        try:
            db = connection.get_connection(config.database)

            start_date        = request.headers.get('start_date', None)
            end_date          = request.headers.get('end_date', None)
            seller_properties = ast.literal_eval(request.headers.get('seller_properties', None))
            status_name       = request.args.get('status', None)
            offset            = int(request.args.get('offset', -1))
            limit             = offset + int(request.args.get('limit', -1))
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
                'seller_properties' : seller_properties,
                'offset'            : offset,
                'limit'             : limit
            }

            payment_complete_order_data = self.service.get_order_informations(db, arguments)

            if (not status_name) or (not start_date) or (not end_date) or (offset == -1) or (limit == -1):
                return jsonify({'message':'KEY_ERROR'}), 400

        except Exception as e:
            return jsonify({'message':e}), 400

        else:
            return jsonify(payment_complete_order_data), 200

        finally:
            db.close()
