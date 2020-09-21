from flask import jsonify

from flask.views import MethodView

# 작성자: 김태수
# 작성일: 2020.09.17.목
# 원산지 데이터와 연결된 class
class CountryOfOriginView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, country_id):
        country_of_origin = self.service.get_country_of_origin(country_id)

        if country_of_origin == None:
            # 요청한 데이터가 존재하지 않는 경우 INVALID_VALUE 에러 전달
            return jsonify({'message':'INVALID_VALUE'}), 400

        return jsonify(country_of_origin), 200
