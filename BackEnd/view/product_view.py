import json
import datetime
import os
from ast import literal_eval

from flask          import jsonify, request, send_file
from flask.views    import MethodView
from pymysql        import err

from botocore.exceptions import ClientError

import traceback

import config
from connection import get_connection
from exceptions import (
    NonImageFilenameError, 
    NonPrimaryImageError,
    ValidationError,
    OneOfDatesAreNoneError,
    ProductIdListEmptyError,
    InvalidDownloadTypeError
)
from utils.validation import (
    validate_products_limit,
    validate_products_offset,
    validate_products_product_id,
    validate_products_seller_property_ids,
    validate_products_start_end_date,
    validate_products_is_sold,
    validate_products_is_displayed,
    validate_products_is_discounted,
    validate_product_code,
    validate_image_status
)
from utils.decorator import login_decorator

class FirstCategoriesBySellerPropertyIdView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        셀러 속성 아이디로 1차 카테고리들을 조회한다.

        Args:

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
            conn = get_connection()

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
            conn = get_connection()

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

class ProductsView(MethodView):
    def __init__(self, service):
        self.service = service

    def post(self):
        """
        상품 등록 뷰 레이어
        데이터베이스 커넥션과 종료를 담당한다. 서비스 & DAO 레이어에서 발생한
        예외처리를 담당한다.

        Args:

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
            2020-09-28(이충희): 초기 생성
            2020-09-29(이충희): 커스텀 에러 처리 추가
        """
        try:
            conn = get_connection()
            
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

    # @login_decorator
    def get(self):
        """
        상품 리스트 조회 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 상품 리스트 리턴
            400: 
                ValidationError: 쿼리스트링 검사 에러
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-30(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            # 필터 조건을 쿼리스트링으로 받아온다.
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

            # 쿼리 스트링 검사
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
            traceback.print_exc()
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class ProductView(MethodView):
    def __init__(self, service):
        self.service = service

    # @login_decorator
    def get(self, code):
        """
        상품 상세 조회 뷰

        Args:
            code: 조회하고 싶은 상품 코드

        Returns:
            200: 
                SUCCESS: 하나의 상품에 대한 상세 정보 리턴
            400: 
                ValidationError: path parameter 검사 에러
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-30(이충희): 초기 생성
        """
        try:
            conn = get_connection()
            validate_product_code(code)

            result = self.service.get_product_by_code(conn, code)
        except ValidationError as e:
            message = { "message": e.message }
            return jsonify(message), 400
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(result), 200
        finally:
            conn.close()

    def post(self, code):
        """
        상품 수정 뷰

        Args:
            code: 수정하고 싶은 상품 아이디

        Returns:
            200: 
                SUCCESS: 하나의 상품에 대한 상세 정보 리턴
            400: 
                NonPrimaryImageError : 대표 이미지 없음 에러
                NonImageFilenameError: 이미지 파일 이름 없음 에러
                ValidationError      : 상품 정보 validation 에러
                KeyError             : 딕셔너리 키 에러
                JSONDecodeError      : 올바른 JSON 형식이 아닌 에러
            500:
                ClientError     : S3 관련 에러
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러
                IntegrityError  : 데이터베이스 무결성 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-04(이충희): 초기 생성
        """

        try:
            conn = get_connection()
            
            # 이미지 업데이트 상태
            # 이미지 파일
            images = []
            for i in range(1, 6):
                image_status = request.form.get(f'image_status_{i}', None)
                image_status = validate_image_status(image_status)
                image = request.files.get(f'image_{i}', None)
                if image_status == "UPLOAD" and not image:
                    raise ValidationError("IMAGE_IS_REQUIRED")

                images.append({"image_status": image_status, "image": image})

            # 수정할 데이터 json body
            body  = json.loads(request.form.get('body', None))
            
            conn.begin()
            
            self.service.update_product(conn, code, images, body)

        except ClientError as e:
            conn.rollback()
            message = { "errno": e.response['Error']['Code'], "errval": e.response['Error']['Message']}
            return jsonify(message), 500
        except (err.OperationalError, err.InternalError, err.IntegrityError) as e:
            conn.rollback()
            message = { "errno": e.args[0], "errval": e.args[1] }
            return jsonify(message), 500
        except (NonPrimaryImageError, NonImageFilenameError, ValidationError) as e:
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


class ProductCountriesView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        원산지 국가 리스트 조회 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 원산지 국가 리스트 리턴
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            results = self.service.get_countries(conn)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class ProductColorsView(MethodView):
    def __init__(self, service):
        self.service = service
    
    def get(self):
        """
        상품 옵션 색상 리스트 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 상품 옵션 색상 리스트 리턴
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희): 초기 생성
        """

        try:
            conn = get_connection()

            results = self.service.get_colors(conn)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class ProductSizesView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        상품 옵션 사이즈 리스트 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 상품 옵션 사이즈 리스트 리턴
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희): 초기 생성
        """

        try:
            conn = get_connection()

            results = self.service.get_sizes(conn)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

class ProductsDownloadView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        상품 리스트 엑셀 다운로드 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 엑셀 파일 다운로드
            400:
                ValidationError         : 상품 아이디 검사 에러
                OneOfDatesAreNoneError  : 시작날짜 종료날짜 중 하나가 없음 에러
                ProductIdListEmptyError : 상품 아이디 리스트가 비었음을 나타내는 에러
                InvalidDownloadTypeError: 다운로드 타입이 all 또는 select가 아닌 에러
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-03(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            # 다운로드 타입 all(날짜 조건의 모든 상품) / select (선택상품)
            download_type = request.args.get('type', '')
            if download_type == "all":
                start_date = request.args.get('start_date', None)
                end_date   = request.args.get('end_date', None)

                if not start_date or not end_date:
                    raise OneOfDatesAreNoneError("BOTH_DATES_MUST_BE_PROVIDED")

                validate_products_start_end_date(start_date, end_date)

                directory, filename, filename_for_user = self.service.make_excel_all(conn, start_date, end_date)
            elif download_type == "select":
                product_ids = literal_eval(request.args.get('product_ids', '[]'))

                if not product_ids:
                    raise ProductIdListEmptyError("PRODUCT_IDS_MUST_BE_PROVIDED")

                for product_id in product_ids:
                    validate_products_product_id(str(product_id))

                directory, filename, filename_for_user = self.service.make_excel_select(conn, tuple(product_ids))
            else:
                raise InvalidDownloadTypeError("TYPE_MUST_BE_ALL_OR_SELECT")

        except (ValidationError, OneOfDatesAreNoneError, ProductIdListEmptyError, InvalidDownloadTypeError)as e:
            message = {"message": e.message}
            return jsonify(message), 400
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            # 액셀 파일 리턴
            now_date = datetime.datetime.now().strftime("%Y%m%d")
            filename_for_user = now_date + "_" + filename_for_user
            return send_file(directory + filename,
                mimetype="application/vnd.ms-excel",
                as_attachment=True,
                attachment_filename=filename_for_user,
                conditional=False)
        finally:
            os.remove(os.path.join('temp/', filename))
            conn.close()

class ProductHistoryView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, product_id):
        """
        상품 이력 조회 뷰

        Args:

        Returns:
            200: 
                SUCCESS: 상품 이력 리스트 리턴
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-03(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            # product_id = int(product_id)
        
            results = self.service.get_product_history(conn, product_id)
            
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500

        else:
            return jsonify(results), 200
        finally:
            conn.close()