import os

from flask          import jsonify, request
from flask.views    import MethodView

from werkzeug.utils import secure_filename

import config
from connection import get_connection

# 작성자: 김태수
# 작성일: 2020.09.17.목
# 원산지 데이터와 연결된 class
class CountryOfOriginView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, country_id):
        try:
            db = connection.get_connection(config.database)
            country_of_origin = self.service.get_country_of_origin(db, country_id)

            if country_of_origin == None:
                # 요청한 데이터가 존재하지 않는 경우 INVALID_VALUE 에러 전달
                return jsonify({'message':'INVALID_VALUE'}), 400

        except:
            db.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400
        else:
            db.commit()
            db.close()
            return jsonify(country_of_origin), 200


class FirstCategoriesBySellerPropertyIdView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        try:
            conn = get_connection(config.database)

            seller_property_id = request.args.get('seller-property-id', None)
            if not seller_property_id or not seller_property_id.isnumeric():
                message = {"message": "INVALID_QUERY_PARAMS"}
                return jsonify(message), 400

            seller_property_id = int(seller_property_id)

            results = self.service.find_first_categories_by_seller_property_id(conn, seller_property_id)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class SecondCategoriesByFirstCategoryIdView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        try:
            conn = get_connection(config.database)

            first_category_id = request.args.get('first-category-id', None)
            if not first_category_id or not first_category_id.isnumeric():
                message = {"message": "INVALID_QUERY_PARAMS"}
                return jsonify(message), 400

            first_category_id = int(first_category_id)

            results = self.service.find_second_categories_by_first_category_id(conn, first_category_id)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class ProductImagesUploadView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        if not request.files:
            message = {"message": "IMAGES_ARE_MISSING"}
            return jsonify(message), 400

        images = request.files.getlist('product_images')
        for image in images:
            if image.filename == '':
                message = {"message": "FILENAME_IS_MISSING"}
                return jsonify(message), 400

            filename = secure_filename(image.filename)
            self.service.upload_image_to_s3(image, filename)

        message = {"message": "UPLOAD_SUCCESS"}
        return jsonify(message), 200

# class ProductCreationView(MethodView):
#     def __init__(self, service):
#         self.service = service

#     def post(self):
#         data = request.get_json()
#         if not data:
#             message = {"message": "JSON_DATA_DOES_NOT_EXISTS"}
#             return jsonify(message), 400
