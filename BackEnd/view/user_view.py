from flask          import jsonify, request
from flask.views    import MethodView

from connection     import get_connection
from pymysql        import err

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

# 유저커뮤니티 검색 기능 endpoint
class  UserSerachView(MethodView):

    def __init__(self, service):
        self.service = service

    @login_decorator
    @catch_exception
    @validate_params(
        Param('id', GET, str, required=False, default=None),
        Param('account_id', GET, str, required=False, default=None),
        Param('user_name', GET, str, required=False, default=None),
        Param('user_phone', GET, str, required=False, default=None),
        Param('user_email', GET, str, required=False,default=None),
        Param('start_date', GET, str, required=False, default=None),
        Param('end_date',GET, str, required=False, default=None),
        Param('page',GET, int, required=False, default=1),
        Param('per_page',GET, int, required=False, default=10),
        Param('order',GET, str, required=False, default='DESC',rules=[Validation_order()])
    )
    def get(self,*args):
        """
        유저커뮤니티 검색 기능 API

        Args:
            search_info :   검색 데이터를 담을 리스트

        Retruns:
            200, results : 해당 검색에 대한 결과
            400, {'message': 'UNSUCCESS'} : 검색실패시

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020.10.01(이지연)  : 초기생성
            2020.10.08(이지연)  : 피드백 반영 ,팀원들과 형식 맞춰 수정
            2020.10.12(이지연)  : 피드백 반영 ,sql delete != 1 → delete = 0로 변경, register_date 날짜 형식 변경

        """
        try:
            conn = connection.get_connection()

            search_info = {
                'id'            : args[0],
                'account_id'    : args[1],
                'user_name'     : args[2],
                'user_phone'    : args[3],
                'user_email'    : args[4],
                'start_date'    : args[5],
                'end_date'      : args[6],
                'page'          : args[7],
                'per_page'      : args[8],
                'order'         : args[9]
            }
            
            results     = self.service.search_user_list(conn, search_info)

        except Exception as e:
            return jsonify({'message': 'UNSUCCESS'}),400
        else:
            return jsonify(results), 200
        finally:
            conn.close()