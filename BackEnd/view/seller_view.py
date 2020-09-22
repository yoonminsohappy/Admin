from flask import jsonify, request

from flask.views import MethodView

class SellerView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        search_term = request.args.get('q')
        limit       = request.args.get('limit', '10')
        
        # 쿼리 파라미터 적절한지 확인
        if not search_term or not limit or not limit.isnumeric():
            message = {"message": "CHECK_QUERY_PARAMS"}
            return jsonify(message), 400

        results     = self.service.search_sellers(search_term, limit)
        return jsonify(results), 200