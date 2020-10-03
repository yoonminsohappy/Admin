from flask          import jsonify, request
from flask.views    import MethodView

from connection     import get_connection
from pymysql        import err

#유효성 검사용 모듈 import
from flask_request_validator import (
    GET,
    PATH,
    FORM,
    Param,
    Pattern,
    JSON,
    validate_params
)

from utils.validation import (
    Validation_order
)

from utils.decorator import (
    login_decorator,
    catch_exception
)

import config,connection

# 검색 기능 endpoint
class  UserSerachView(MethodView):

    def __init__(self, service):
        self.service = service

    @catch_exception
    @validate_params(
        Param('id', GET, str, required=False, default=''),
        Param('account_id', GET, str, required=False, default=''),
        Param('user_name', GET, str, required=False, default=''),
        Param('user_phone', GET, str, required=False, default=''),
        Param('user_email', GET, str, required=False,default=''),
        Param('from', GET, str, required=False, default=''),
        Param('to',GET, str, required=False, default=''),
        Param('page',GET, int, required=False, default=1),
        Param('order',GET, str, required=False, default='DESC',rules=[Validation_order()])
    )
    def get(self,*args):
        try:
            conn = connection.get_connection(config.database)

            search_info = {
                'id'            : args[0],
                'account_id'    : args[1],
                'user_name'     : args[2],
                'user_phone'    : args[3],
                'user_email'    : args[4],
                'from'          : args[5],
                'to'            : args[6],
                'page'          : args[7],
                'order'         : args[8]
            }
            
            results     = self.service.search_user_list(conn, search_info)

        except Exception as e:
            return jsonify({'message': str(e)}),400
        else:
            return jsonify(results), 200
        finally:
            conn.close()