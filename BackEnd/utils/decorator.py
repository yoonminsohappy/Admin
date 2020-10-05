import bcrypt
import jwt 

from functools        import wraps
from flask            import request,Response,jsonify
from model.seller_dao import SellerDao
from connection       import get_connection

import traceback

import config,connection

def login_decorator(f):

    """
        decorator API

            Args:
                에러 받는다.

            Retruns:
                return f(*args, **kwargs) -> 데코레이터를 발행해준다.
                return jsonify({'message':'INVALID_USER'}), 400 -> 올바르지 않은 user의 메세지와 400에러
                return jsonify({'message':'INVALID_TOKEN'}), 400 -> 올바르지 않은 토큰과 400에러

            Authors:
                wldus9503@gmail.com(이지연)
            
            History:
                2020.09.24(이지연) : 데코레이터 초기 생성
                2020.09.28(이지연) : 유효성 검사 customexception -> validationexception 변경
                2020.09.29(이지연) : 클래스 Validation_order 추가, DB ORDER기능 위한것
                2020.10.05(이지연) : 데코레이터 
    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            #Authorization Header에 담긴 Access Token, csrf 등 보안공격에 대해서 안전
            access_token = request.headers.get('Authorization', None)
            
            if access_token :                 
                #access_token을 복호화 하여 payload JSON을 읽어 들인다. jwt 모듈의 decode 함수는 JWT access_token을
                # 복호화할 뿐만 아니라 토큰이 해당 백엔드 API서버에서 생선된 token인지를 확인하는 절차를 밟는다.
                # 그래서 'JWT_SECRET_KEY'에서 필드 값을 읽어 들여 secret key를 읽고 
                # 'HS256'으로 동일하게 복호화해서 결과가 같은지를 확인한다.
                payload         = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.ALGORITHM)
                seller_account  = payload['seller_account']

                conn            = connection.get_connection(config.database)
                # seller_account의 value값과 db에 연결에서 실제 있는지 확인하기 위한 용도
                result = SellerDao().select_seller(seller_account,conn)

                conn.close() #db 연결 종료
                if result:
                    request.user = result
                    return f(*args, **kwargs)
                return jsonify({'message':'INVALID_USER'}), 400
        except jwt.exceptions.DecodeError:
            traceback.print_exc()
            return jsonify({'message':'INVALID_TOKEN'}), 400
    return wrapper

def catch_exception(f, *args, **kwargs):

    """
        decorator API

            Args:
                에러들을 받는다.

            Retruns:
                return f(*args, **kwargs) -> 데코레이터를 발행해준다.
                jsonify({"message" : f"INVALID_PARAMETER_{e.args[0]}"}), 400 -> 해당 에러 메시지 내용과 400에러

            Authors:
                wldus9503@gmail.com(이지연)
            
            History:
                2020 - 09 - 29(wldus9503@gmail.com) : 데코레이터 초기 생성
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            if len(e.args)==0:
                return jsonify({"message" : "INVALID_PARAMETER"}), 400
            return jsonify({"message" : f"INVALID_PARAMETER_{e.args[0]}"}), 405
    return wrapper