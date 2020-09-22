from flask import jsonify, request

from flask.views import MethodView

# 작성자: 김태수
# 작성일: 2020.09.17.목
# 원산지 데이터와 연결된 class
class CountryOfOriginView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, country_id):
        try:
            country_of_origin = self.service.get_country_of_origin(country_id)

            if country_of_origin == None:
                # 요청한 데이터가 존재하지 않는 경우 INVALID_VALUE 에러 전달
                return jsonify({'message':'INVALID_VALUE'}), 400

            return jsonify(country_of_origin), 200

        except:
            return jsonify({'message':'UNSUCCESS'}), 400

class FirstCategoriesBySellerPropertyIdView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        data = request.get_json()
        if not data:
            message = {"message": "JSON_DATA_DOES_NOT_EXISTS"}
            return jsonify(message), 400

        seller_property_id = data.get('seller_property_id', None)
        if not seller_property_id:
            message = {"message": "INVALID_FORM_DATA"}
            return jsonify(message), 400

        results = self.service.find_first_categories_by_seller_property_id(seller_property_id)
        return jsonify(results), 200

class SecondCategoriesByFirstCategoryIdView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        data = request.get_json()
        if not data:
            message = {"message": "JSON_DATA_DOES_NOT_EXISTS"}
            return jsonify(message), 400

        first_category_id = data.get('first_category_id', None)
        if not first_category_id:
            message = {"message": "INVALID_FORM_DATA"}
            return jsonify(message), 400

        results = self.service.find_second_categories_by_first_category_id(first_category_id)
        return jsonify(results), 200