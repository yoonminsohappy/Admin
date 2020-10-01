import json
from ast import literal_eval

from flask          import jsonify, request
from flask.views    import MethodView
from pymysql        import err

from botocore.exceptions import ClientError

import config
from connection import get_connection
from exceptions import (
    NonImageFilenameError, 
    NonPrimaryImageError,
    ValidationError
)
from utils.validation import (
    validate_products_limit,
    validate_products_offset,
    validate_products_product_id,
    validate_products_seller_property_ids,
    validate_products_start_end_date,
    validate_products_is_sold,
    validate_products_is_displayed,
    validate_products_is_discounted
)

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
        """
        셀러 속성 아이디로 1차 카테고리들을 조회한다.

        Args:
            service: 서비스 레이어 객체

        Returns:
            200: 
                1차 카테고리 딕셔너리 리스트를 JSON으로 리턴
            400: 
                INVALID_QUERY_PARAMS: 쿼리 스트링의 값이 올바르지 않음
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러
                
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
        """
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
        """
        1차 카테고리 아이디로 2차 카테고리들을 조회한다.

        Args:
            service: 서비스 레이어 객체

        Returns:
            200: 
                2차 카테고리 딕셔너리 리스트를 JSON으로 리턴
            400: 
                INVALID_QUERY_PARAMS: 쿼리 스트링의 값이 올바르지 않음
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러
                
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
        """
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

class ProductCreationView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        """
        상품 등록 뷰 레이어
        데이터베이스 커넥션과 종료를 담당한다. 서비스 & DAO 레이어에서 발생한
        예외처리를 담당한다.

        Args:
            service: 서비스 레이어 객체

        Returns:
            200: 
                SUCCESS: 상품 등록 성공
            400: 
                JSONDecodeError      : 올바른 JSON 형식이 아님
                KeyError             : JSON 딕셔너리 키값이 없음
                NonImageFilenameError: 파일 이름이 없음
                NonPrimaryImageError : 대표 상품 이미지가 없음
            500:
                ClientError     : S3 에러
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러
                IntegrityError  : 데이터베이스 무결성 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
            2020-09-29(이충희): 커스텀 에러 처리 추가
        """
        try:
            conn = get_connection(config.database)
            
            images = []
            for i in range(1, 6):
                image = request.files.get(f'image_{i}', None)
                images.append(image)

            body  = json.loads(request.form.get('body', None))
            
            conn.begin()
            self.service.add_product(conn, images, body)

        except ClientError as e:
            conn.rollback()
            message = { "errno": e.response['Error']['Code'], "errval": e.response['Error']['Message']}
            return jsonify(message), 500
        except (err.OperationalError, err.InternalError, err.IntegrityError) as e:
            conn.rollback()
            message = { "errno": e.args[0], "errval": e.args[1] }
            return jsonify(message), 500
        except (NonPrimaryImageError, NonImageFilenameError) as e:
            conn.rollback()
            message = { "message": e.message }
            return jsonify(message), 400
        except KeyError as e:
            conn.rollback()
            message = { "message": "FORM_DATA_KEY_ERROR" }
            return jsonify(message), 400
        except json.decoder.JSONDecodeError as e:
            db_connection.rollback()
            message = { "message": "INVALID_JSON_FORMAT" }
            return jsonify(message), 400
        else:
            conn.commit()
            message = { "message": "SUCCESS" }
            return jsonify(message), 200
        finally:
            conn.close()

    def get(self):
        try:
            conn                = get_connection(config.database)
            limit               = request.args.get('limit', '10')
            offset              = request.args.get('offset', '0')
            start_date          = request.args.get('start_date', None)
            end_date            = request.args.get('end_date', None)
            seller_name         = request.args.get('seller_name', None)
            product_name        = request.args.get('product_name', None)
            product_id          = request.args.get('product_number', None)
            product_code        = request.args.get('product_code', None)
            seller_property_ids = literal_eval(request.args.get('seller_property_ids', '[]'))
            is_sold             = request.args.get('is_sold', None)
            is_displayed        = request.args.get('is_displayed', None)
            is_discounted       = request.args.get('is_discounted', None)

            limit  = validate_products_limit(limit)
            offset = validate_products_offset(offset)
            validate_products_start_end_date(start_date, end_date)
            product_id    = validate_products_product_id(product_id)
            is_sold       = validate_products_is_sold(is_sold)
            is_displayed  = validate_products_is_displayed(is_displayed)
            is_discounted = validate_products_is_discounted(is_discounted)
            validate_products_seller_property_ids(seller_property_ids)
            
            results = self.service.get_products_list(
                conn, 
                limit, 
                offset,
                start_date,
                end_date,
                seller_name,
                product_name,
                product_id,
                product_code,
                seller_property_ids,
                is_sold,
                is_displayed,
                is_discounted
            )
        except ValidationError as e:
            message = {"message": e.message}
            return jsonify(message), 400
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()