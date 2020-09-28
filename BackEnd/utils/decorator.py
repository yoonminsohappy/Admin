import bcrypt
import jwt 

from functools        import wraps
from flask            import request,Response,jsonify
from model.seller_dao import SellerDao
from connection       import get_connection

import config,connection

def login_decorator(f):
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
                    return f(*args, **kwargs)
                return jsonify({'message':'INVALID_USER'}), 400
        except jwt.exceptions.DecodeError:
            return jsonify({'message':'INVALID_TOKEN'}), 401
    return wrapper