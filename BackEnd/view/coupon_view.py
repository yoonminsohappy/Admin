import os
import datetime
import traceback
from json.decoder import JSONDecodeError

from flask       import jsonify, request, send_file
from flask.views import MethodView
from pymysql     import err
from varname     import Wrapper

import config
from connection import get_connection
from utils.validation import (
    CouponValidationError,
    validate_coupon_int_required,
    validate_coupon_int_optional,
    validate_coupon_str_required,
    validate_coupon_str_optional,
    validate_coupon_date_optional,
    validate_coupon_bool_optional
)

class VarnameException(Exception):
    def __init__(self, message, var):
        self.message = message
        self.var     = var

    def to_dict(self):
        return {
            "message" : self.message,
            "varname" : self.var.name,
            "varvalue": self.var.value
        }

class NonePointerException(VarnameException):
    def __init__(self, message, var):
        super().__init__(message, var)
    
class NumberFormatException(VarnameException):
    def __init__(self, message, var):
        super().__init__(message, var)

class DateFormatException(VarnameException):
    def __init__(self, message, var):
        super().__init__(message, var)
        
class IncompatibleDatetimesException(VarnameException):
    def __init__(self, message, var, var2):
        self.message = message
        self.var     = var
        self.var2    = var2

    def to_dict(self):
        return {
            "message"  : self.message,
            "varname1" : self.var.name,
            "varvalue1": self.var.value,
            "varname2" : self.var2.name,
            "varvalue2": self.var2.value
        }

class CouponsView(MethodView):
    def __init__(self, service):
        self.service = service

    def check_null_or_empty(self, data):
        if not data:
            raise NonePointerException("DATA_IS_NONE", data)

    def validate_integer(self, number):
        self.check_null_or_empty(number)

        if not isinstance(number.value, int):
            raise NumberFormatException("NOT A NUMBER", number)

    def validate_datetime_format(self, my_datetime):
        try:
            return datetime.datetime.strptime(my_datetime.value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise DateFormatException("DATE_FORMAT_IS_WRONG", my_datetime)
    
    def compare_two_datetimes(self, str_datetime_one, str_datetime_two):
        self.check_null_or_empty(str_datetime_one)
        self.check_null_or_empty(str_datetime_two)

        datetime_one = self.validate_datetime_format(str_datetime_one)
        datetime_two = self.validate_datetime_format(str_datetime_two)

        if datetime_one >= datetime_two:
            raise IncompatibleDatetimesException(
                "START_DATETIME_CANNOT_BE_GREATHAER_THAN_END_ONE", 
                str_datetime_one, str_datetime_two,
            )

    def validate_positive_number(self, data):
        self.validate_integer(data)

        if data.value < 0:
            raise NumberFormatException("POSITIVE_NUMBER_PLEASE", data)

    def validate_issue_id_and_code(self, issue_id, code):
        ISSUE_TYPE_COUPON_CODE = 2

        self.validate_positive_number(issue_id)
        self.check_null_or_empty(code)
        
        if issue_id.value == ISSUE_TYPE_COUPON_CODE and not code.value:
            raise NonePointerException(f"COUPON_CODE_REQUIRED", code)

    def check_has_condition(self, params):
        if params['id'] or \
        params['name'] or \
        params['valid_started_from'] or \
        params['valid_started_to'] or \
        params['valid_ended_from'] or \
        params['valid_ended_to'] or \
        params['download_started_from'] or \
        params['download_started_to'] or \
        params['download_ended_from'] or \
        params['download_ended_to'] or \
        params['issue_type_id'] or \
        params['is_limited'] == 'Y' or \
        params['is_limited'] == 'N':
            return True

        return False
            
    def post(self):
        """
        쿠폰 등록

        Args:

        Returns:
            200: 상품 등록 성공
            400: 유효성 검사 에러, 타입 에러 (널), 딕셔너리 키 에러, JSON 형식 에러
            500: 데이터베이스 조작 에러, 내부 에러, 무결성 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-09(이충희): 초기 생성
        """
        ISSUE_TYPE_SERIAL_NUMBER = 3

        try:
            conn = get_connection()

            data = request.get_json()
            
            name                     = Wrapper(data['name'])
            type_id                  = Wrapper(data['type_id'])
            is_downloadable          = Wrapper(data['is_downloadable'])
            issue_id                 = Wrapper(data['issue_id'])
            code                     = Wrapper(data['code'])
            description              = Wrapper(data['description'])
            download_started_at      = Wrapper(data['download_started_at'])
            download_ended_at        = Wrapper(data['download_ended_at'])
            valid_started_at         = Wrapper(data['valid_started_at'])
            valid_ended_at           = Wrapper(data['valid_ended_at'])
            discount_price           = Wrapper(data['discount_price'])
            limit_count              = Wrapper(data['limit_count'])
            minimum_price            = Wrapper(data['minimum_price'])

            self.check_null_or_empty(name)
            self.validate_positive_number(type_id)
            self.validate_positive_number(is_downloadable)
            self.validate_issue_id_and_code(issue_id, code)
            self.check_null_or_empty(description)
            self.compare_two_datetimes(valid_started_at, valid_ended_at)
            self.validate_positive_number(discount_price)
            if download_started_at.value and download_ended_at.value:
                self.compare_two_datetimes(download_started_at, download_ended_at)
            self.validate_positive_number(limit_count)
            self.validate_positive_number(minimum_price)

            self.service.make_coupon(conn, data)

        except (err.OperationalError, err.InternalError, err.IntegrityError) as e:
            conn.rollback()
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except VarnameException as e:
            return jsonify(e.to_dict()), 400

        except TypeError as e:
            conn.rollback()
            return jsonify({"message": e.args[0]}), 400

        except KeyError as e:
            return jsonify({"message": "KEY_ERROR", "key_name": e.args[0]}), 400

        except JSONDecodeError:
            return jsonify({"message": "INVALID_JSON_FORMAT"}), 400

        else:
            conn.commit()
            return jsonify({"message": "SUCCESS"}), 200

        finally:
            conn.close()

    def get(self):
        """
        쿠폰 조회

        Args:

        Returns:
            200: 상품 JSON 리턴
            400: 쿼리 스트링 유효성 검사 에러
            500: 데이터베이스 조작 에러, 내부 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-10(이충희): 초기 생성
        """
        KEY_LIMIT                 = 'limit'
        KEY_PAGE                  = 'page'
        KEY_ID                    = 'id'
        KEY_NAME                  = 'name'
        KEY_VALID_STARTED_FROM    = 'valid_started_from'
        KEY_VALID_STARTED_TO      = 'valid_started_to'
        KEY_VALID_ENDED_FROM      = 'valid_ended_from'
        KEY_VALID_ENDED_TO        = 'valid_ended_to'
        KEY_DOWNLOAD_STARTED_FROM = 'download_started_from'
        KEY_DOWNLOAD_STARTED_TO   = 'download_started_to'
        KEY_DOWNLOAD_ENDED_FROM   = 'download_ended_from'
        KEY_DOWNLOAD_ENDED_TO     = 'download_ended_to'
        KEY_ISSUE_TYPE_ID         = 'issue_type_id'
        KEY_IS_LIMITED            = 'is_limited'
        KEY_OFFSET                = 'offset'
        KEY_HAS_CONDITION         = 'has_condition'
        TIME_DAY_BEGIN            = ' 00:00:00'
        TIME_DAY_END              = ' 23:59:59'

        try:
            conn = get_connection()

            limit                 = request.args.get(KEY_LIMIT, 10)
            page                  = request.args.get(KEY_PAGE, 1)
            coupon_id             = request.args.get(KEY_ID, None)
            coupon_name           = request.args.get(KEY_NAME, None)
            valid_started_from    = request.args.get(KEY_VALID_STARTED_FROM, None)
            valid_started_to      = request.args.get(KEY_VALID_STARTED_TO, None)
            valid_ended_from      = request.args.get(KEY_VALID_ENDED_FROM, None)
            valid_ended_to        = request.args.get(KEY_VALID_ENDED_TO, None)
            download_started_from = request.args.get(KEY_DOWNLOAD_STARTED_FROM, None)
            download_started_to   = request.args.get(KEY_DOWNLOAD_STARTED_TO, None)
            download_ended_from   = request.args.get(KEY_DOWNLOAD_ENDED_FROM, None)
            download_ended_to     = request.args.get(KEY_DOWNLOAD_ENDED_TO, None)
            issue_type_id         = request.args.get(KEY_ISSUE_TYPE_ID, None)
            is_limited            = request.args.get(KEY_IS_LIMITED, None) # Y, N

            # validation
            limit = validate_coupon_int_required(limit, KEY_LIMIT)
            if limit not in [10, 20, 50]:
                limit = 10

            page = validate_coupon_int_required(page, KEY_PAGE)
            if page <= 0:
                page = 1

            coupon_id             = validate_coupon_int_optional(coupon_id, KEY_ID)
            coupon_name           = validate_coupon_str_optional(coupon_name, KEY_NAME)
            valid_started_from    = validate_coupon_date_optional(valid_started_from, KEY_VALID_STARTED_FROM)
            valid_started_to      = validate_coupon_date_optional(valid_started_to, KEY_VALID_STARTED_TO)
            valid_ended_from      = validate_coupon_date_optional(valid_ended_from, KEY_VALID_ENDED_FROM)
            valid_ended_to        = validate_coupon_date_optional(valid_ended_to, KEY_VALID_ENDED_TO)
            download_started_from = validate_coupon_date_optional(download_started_from, KEY_DOWNLOAD_STARTED_FROM)
            download_started_to   = validate_coupon_date_optional(download_started_to, KEY_DOWNLOAD_STARTED_TO)
            download_ended_from   = validate_coupon_date_optional(download_ended_from, KEY_DOWNLOAD_ENDED_FROM)
            download_ended_to     = validate_coupon_date_optional(download_ended_to, KEY_DOWNLOAD_ENDED_TO)
            issue_type_id         = validate_coupon_int_optional(issue_type_id, KEY_ISSUE_TYPE_ID)
            is_limited            = validate_coupon_bool_optional(is_limited, KEY_IS_LIMITED)

            # to params
            params = {}
            params[KEY_LIMIT]                 = limit
            params[KEY_OFFSET]                = (page - 1) * limit
            params[KEY_ID]                    = coupon_id
            params[KEY_NAME]                  = '%%' + coupon_name + '%%' if coupon_name else coupon_name
            params[KEY_VALID_STARTED_FROM]    = valid_started_from + TIME_DAY_BEGIN if valid_started_from else valid_started_from
            params[KEY_VALID_STARTED_TO]      = valid_started_to + TIME_DAY_END if valid_started_to else valid_started_to
            params[KEY_VALID_ENDED_FROM]      = valid_ended_from + TIME_DAY_BEGIN if valid_ended_from else valid_ended_from
            params[KEY_VALID_ENDED_TO]        = valid_ended_to + TIME_DAY_END if valid_ended_to else valid_ended_to
            params[KEY_DOWNLOAD_STARTED_FROM] = download_started_from + TIME_DAY_BEGIN if download_started_from else download_started_from
            params[KEY_DOWNLOAD_STARTED_TO]   = download_started_to + TIME_DAY_END if download_started_to else download_started_to
            params[KEY_DOWNLOAD_ENDED_FROM]   = download_ended_from + TIME_DAY_BEGIN if download_ended_from else download_ended_from
            params[KEY_DOWNLOAD_ENDED_TO]     = download_ended_to + TIME_DAY_END if download_ended_to else download_ended_to
            params[KEY_ISSUE_TYPE_ID]         = issue_type_id
            params[KEY_IS_LIMITED]            = is_limited
            params[KEY_HAS_CONDITION]         = self.check_has_condition(params)

            results = self.service.get_coupons(conn, params)

        except CouponValidationError as e:
            return jsonify(e.to_dict()), 400
        
        except (err.OperationalError, err.InternalError) as e: 
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        else: 
            return jsonify(results), 200

        finally:
            conn.close()

class CouponSerialsView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, coupon_id):
        """
        쿠폰 시리얼 넘버 CSV 다운로드

        Args:
            coupon_id: 쿠폰 아이디

        Returns:
            200: 시리얼 넘버를 담은 CSV 파일 리턴
            400: 존재하지 않는 쿠폰 아이디로 쿠폰 조회
            500: 데이터베이스 조작 에러, 내부 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-11(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            coupon_id = validate_coupon_int_required(coupon_id, 'coupon_id')

            tmp_filename, download_filename = self.service.download_serials(conn, coupon_id)

        except (err.OperationalError, err.InternalError) as e: 
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except TypeError as e:
            return jsonify({"message": e.args[0]}), 400

        else: 
            file_to_send = send_file(tmp_filename, mimetype="text/csv",
                as_attachment=True, attachment_filename=download_filename, conditional=False)
            os.remove(tmp_filename)
            return file_to_send
            
        finally:
            conn.close()

class CouponView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, coupon_id):
        """
        쿠폰 조회

        Args:

        Returns:
            200: 상품 JSON 리턴
            400: 쿼리 스트링 유효성 검사 에러
            500: 데이터베이스 조작 에러, 내부 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-10(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            coupon_id = validate_coupon_int_required(coupon_id, 'coupon_id')

            result = self.service.get_coupon_info(conn, coupon_id)
            
        except (err.OperationalError, err.InternalError) as e: 
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except TypeError as e:
            return jsonify({"message": e.args[0]}), 400

        else: 
            return jsonify(result), 200

        finally:
            conn.close()

    def put(self, coupon_id):
        """
        쿠폰 수정

        Args:
            coupon_id: 수정할 쿠폰 아이디

        Returns:
            200: 시리얼 넘버를 담은 CSV 파일 리턴
            400: 존재하지 않는 쿠폰 아이디로 쿠폰 조회, 딕셔너리 키에러
            500: 데이터베이스 조작 에러, 내부 에러, 무결성 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-11(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            data = request.get_json()
            
            coupon_name = data['coupon_name']
            description = data['description']

            coupon_id   = validate_coupon_int_required(coupon_id, 'coupon_id')
            coupon_name = validate_coupon_str_required(coupon_name, 'coupon_name')
            description = validate_coupon_str_required(description, 'description')

            params = {}
            params['coupon_id']   = coupon_id
            params['coupon_name'] = coupon_name
            params['description'] = description

            self.service.update_coupon_info(conn, params)
            
        except (err.OperationalError, err.InternalError, err.IntegrityError) as e: 
            conn.rollback()
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except TypeError as e:
            conn.rollback()
            return jsonify({"message": e.args[0]}), 400

        except KeyError as e:
            return jsonify({"message": "KEY_ERROR", "key_name": e.args[0]}), 400

        else: 
            conn.commit()
            return jsonify({"message": "SUCCESS"}), 200

        finally:
            conn.close()


    def delete(self, coupon_id):
        """
        쿠폰 삭제

        Args:
            coupon_id: 삭제할 쿠폰 아이디

        Returns:
            200: 삭제 성공 메시지
            400: 존재하지 않는 쿠폰 아이디로 쿠폰 조회
            500: 데이터베이스 조작 에러, 내부 에러, 무결성 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-11(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            coupon_id = validate_coupon_int_required(coupon_id, 'coupon_id')

            self.service.remove_coupon(conn, coupon_id)
            
        except (err.OperationalError, err.InternalError, err.IntegrityError) as e: 
            conn.rollback()
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except TypeError as e:
            return jsonify({"message": e.args[0]}), 400

        else: 
            conn.commit()
            return jsonify({"message": "SUCCESS"}), 200

        finally:
            conn.close()

class CouponCodeView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self, coupon_id):
        """
        쿠폰 코드 조회

        Args:
            coupon_id: 조회할 쿠폰 아이디

        Returns:
            200: 쿠폰 코드 리턴
            400: 존재하지 않는 쿠폰 아이디로 쿠폰 조회
            500: 데이터베이스 조작 에러, 내부 에러
            
        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-11(이충희): 초기 생성
        """
        try:
            conn = get_connection()

            coupon_id = validate_coupon_int_required(coupon_id, 'coupon_id')
 
            result = self.service.get_coupon_code(conn, coupon_id)

        except (err.OperationalError, err.InternalError) as e: 
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except TypeError as e:
            return jsonify({"message": e.args[0]}), 400

        else: 
            return jsonify(result), 200
            
        finally:
            conn.close()