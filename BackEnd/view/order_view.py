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

            day = timedelta(days = 1)
            end_date = date.fromisoformat(end_date) + day

            seller_properties = list(map(int, seller_properties))

            payment_complete_order_data = self.service.get_order_informations(db, status_name, start_date, end_date, offset, limit)

        except:
            db.close()
            return jsonify({'message':'UNSUCCESS'}), 400
        else:
            db.close()
            return jsonify(payment_complete_order_data), 200
