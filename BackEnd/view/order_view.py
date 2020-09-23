from flask import jsonify, request

from flask.views import MethodView

# 작성자: 김태수
# 작성일: 2020.09.17.목
# 원산지 데이터와 연결된 class
class OrderDataView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        try:
            status_name = request.args.get('status_name')
            offset   = int(request.args.get('offset'))
            limit    = offset + int(request.args.get('limit'))
            order_data = self.service.get_order_informations(status_name, offset, limit)

            if order_data == None:
                # 요청한 데이터가 존재하지 않는 경우 INVALID_VALUE 에러 전달
                return jsonify({'message':'INVALID_VALUE'}), 400

            return jsonify(order_data), 200

        except:
            return jsonify({'message':'UNSUCCESS'}), 400
