import datetime
import traceback
from json.decoder import JSONDecodeError

from flask       import jsonify, request
from flask.views import MethodView
from pymysql     import err
from varname     import Wrapper

import config
from connection import get_connection

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
            
    def post(self):
        ISSUE_TYPE_SERIAL_NUMBER = 3

        try:
            conn = get_connection(config.database)

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
            is_limited_coupon        = Wrapper(data['is_limited_coupon'])
            limit_count              = Wrapper(data['limit_count'])
            is_limited_minimum_price = Wrapper(data['is_limited_minimum_price'])
            minimum_price            = Wrapper(data['minimum_price'])

            self.check_null_or_empty(name)
            self.validate_positive_number(type_id)
            self.validate_positive_number(is_downloadable)
            self.validate_issue_id_and_code(issue_id, code)
            self.check_null_or_empty(description)
            self.compare_two_datetimes(valid_started_at, valid_ended_at)
            self.validate_positive_number(discount_price)
            self.validate_positive_number(is_limited_coupon)
            self.validate_positive_number(is_limited_minimum_price)

            if download_started_at.value and download_ended_at.value:
                self.compare_two_datetimes(download_started_at, download_ended_at)

            if not is_limited_coupon.value:
                data['limit_count'] = None
            else:
                self.validate_positive_number(limit_count)

            if not is_limited_minimum_price.value:
                data['minimum_price'] = None
            else:
                self.validate_positive_number(minimum_price)

            self.service.make_coupon(conn, data)

        except (err.OperationalError, err.InternalError, err.IntegrityError) as e:
            traceback.print_exc()
            conn.rollback()
            return jsonify({ "errno": e.args[0], "errval": e.args[1] }), 500

        except VarnameException as e:
            return jsonify(e.to_dict()), 400

        except KeyError as e:
            return jsonify({"message": "KEY_ERROR", "key_name": e.args[0]}), 400

        except JSONDecodeError:
            return jsonify({"message": "INVALID_JSON_FORMAT"}), 400

        else:
            conn.commit()
            return jsonify({"message": "SUCCESS"}), 200

        finally:
            conn.close()