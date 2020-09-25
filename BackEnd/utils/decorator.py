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
            access_token = request.headers.get('Authorization', None)
            
            if access_token :                 
                payload         = jwt.decode(access_token, config.SECRET_KEY, algorithm = config.ALGORITHM)
                seller_account  = payload['seller_account']

                conn            = connection.get_connection(config.database)
                
                result = SellerDao().select_seller(seller_account,conn)
                if result:
                    return f(*args, **kwargs)
                return jsonify({'message':'INVALID_USER'}), 400
        except jwt.exceptions.DecodeError:
            return jsonify({'message':'INVALID_TOKEN'}), 401
    return wrapper