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
                2020.10.05(이지연) : 데코레이터 수정
                2020.10.07(이지연) : 데코레이터 수정 -> 로그인시 데코레이터 계정로그인에서 pk로 payloaad불러오기
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            #Authorization Header에 담긴 Access Token, csrf 등 보안공격에 대해서 안전
            access_token = request.headers.get('Authorization', None)
            if access_token :             
                payload         = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.ALGORITHM)
                #seller_id 즉 sellers테이블의 pk를 payload로 불러오기
                seller_id  = payload['seller_id']
                conn       = connection.get_connection()
                # seller_id의 value값과 db에 연결에서 실제 있는지 확인하기 위한 용도
                result = SellerDao().decorator_find_seller(conn, seller_id)
                conn.close() #db 연결 종료
                if result:
                    #request의 seller_id 라는 속성에는 seller_id값을 넣어주도록합니다
                    request.seller_id = seller_id
                    # result를 request(http요청)의 user라는 속성에 넣어주도록합니다.
                    request.user = result
                    #이후 로그인한 유저에 대한 정보가 추가된 request를 포함시켜서 return
                    return f(self, *args)
                return jsonify({'message':'INVALID_USER'}), 400
        except jwt.exceptions.DecodeError:
            traceback.print_exc()
            return jsonify({'message':'INVALID_TOKEN'}), 400
    return wrapper

def login_decorator2(f):

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
                2020.10.05(이지연) : 데코레이터 수정
                2020.10.07(이지연) : 데코레이터 수정 -> 로그인시 데코레이터 계정로그인에서 pk로 payloaad불러오기
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):

        try:
            #Authorization Header에 담긴 Access Token, csrf 등 보안공격에 대해서 안전
            access_token = request.headers.get('Authorization', None)

            if access_token :             
                payload         = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.ALGORITHM)
                
                #seller_id 즉 sellers테이블의 pk를 payload로 불러오기
                seller_id  = payload['seller_id']
                conn       = connection.get_connection()

                kwargs['seller_id'] = seller_id

                # seller_id의 value값과 db에 연결에서 실제 있는지 확인하기 위한 용도
                result = SellerDao().decorator_find_seller(conn, seller_id)

                conn.close() #db 연결 종료

                if result:
                    #request의 seller_id 라는 속성에는 seller_id값을 넣어주도록합니다
                    request.seller_id = seller_id
                    # result를 request(http요청)의 user라는 속성에 넣어주도록합니다.
                    request.user = result
                    
                    #이후 로그인한 유저에 대한 정보가 추가된 request를 포함시켜서 return
                    return f(self, *args, **kwargs)
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