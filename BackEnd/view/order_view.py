from flask import jsonify, request
from flask.views import MethodView

from datetime import date, timedelta

import config, connection

# 작성자: 김태수
# 작성일: 2020.09.17.목
class GetOrderDataView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        try:
            db = connection.get_connection(config.database)
            start_date = request.headers.get('start_date')
            end_date = request.headers.get('end_date')
            seller_properties = request.headers.get('seller_properties', None)
            status_name       = request.args.get('status')
            offset            = int(request.args.get('offset'))
            limit             = offset + int(request.args.get('limit'))
            order_number      = "%" + request.args.get('order_number', "") + "%"
            detail_number     = "%" + request.args.get('detail_number', "") + "%"
            user_name         = "%" + request.args.get('user_name', "") + "%"
            phone_number      = "%" + request.args.get('phone_number', "") + "%"
            seller_name       = "%" + request.args.get('seller_name', "") + "%"
            product_name      = "%" + request.args.get('product_name', "") + "%"

            day = timedelta(days = 1)
            end_date = date.fromisoformat(end_date) + day

            seller_properties = tuple(map(int, seller_properties))

            arguments = (start_date, end_date, status_name, order_number, detail_number, user_name, phone_number, seller_name, product_name, seller_properties, offset, limit)

            payment_complete_order_data = self.service.get_order_informations(db, arguments)

        except:
            return jsonify({'message':'UNSUCCESS'}), 400
        else:
            return jsonify(payment_complete_order_data), 200
        finally:
            db.close()
