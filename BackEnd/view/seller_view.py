from flask          import jsonify, request
from flask.views    import MethodView

from connection     import get_connection
from pymysql        import err

from utils.decorator import login_decorator

import config,connection

class ProductSellerSearchView(MethodView):
    def __init__(self, service):
        self.service = service

    @login_decorator
    def get(self):
        try: 
            conn        = get_connection(config.database)
        
            search_term = request.args.get('q')
            limit       = request.args.get('limit', '10')
    
            if not search_term or not limit or not limit.isnumeric():
                message = {"message": "CHECK_QUERY_PARAMS"}
                return jsonify(message), 400

            limit = int(limit)
            if limit > 10:
                limit = 10
            
            results     = self.service.search_sellers(conn, search_term, limit)
        except (err.OperationalError, err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 500
        else:
            return jsonify(results), 200
        finally:
            conn.close()

# 작성자: 이지연
# 작성일: 2020.09.22.화
# 회원가입 endpoint

class SellerSignUpView(MethodView):  
    def __init__(self, service):
        self.service = service 

    def post(self):
        try:
            conn          = connection.get_connection(config.database)
            seller_info   = request.get_json()
            sign_up       = self.service.sign_up(seller_info, conn)
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 400
        except Exception as e:
            conn.rollback()
            return jsonify({'message':'UNSUCCESS'}), 400
        else:
            conn.commit()    
            return jsonify({'message':'SUCCESS'}), 200 
        finally:
            conn.close()  
            
# 작성자: 이지연
# 작성일: 2020.09.23.화
# 로그인 endpoint

class SellerSignInView(MethodView): 
    def __init__(self, service):
        self.service = service 

    def post(self):
        try:
            conn          = connection.get_connection(config.database)
            seller_info   = request.get_json()
            access_token  = self.service.sign_in(seller_info,conn)
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 400
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'UNSUCCESS'}),400
        else:
            conn.commit()
            return jsonify({'access_token':access_token}),200
        finally:
            conn.close() 

