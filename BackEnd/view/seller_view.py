from flask       import jsonify, request
from flask.views import MethodView

from pymysql import err

import config
from connection import get_connection

class ProductSellerSearchView(MethodView):
    def __init__(self, service):
        self.service = service

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

class SellerSignUpView(MethodView):  # 특정 메서드에 요청을 전달/요청에 응답
    def __init__(self, service):
        self.service = service #메소드별로 사용할 수 있도록 해당 service변수에 service를 넣어줌

    def post(self):
        data = request.get_json() #http body json형태로 변경
        
        result = self.service.sign_up(data)
        if result:
            print(result)
            message  = {"message" : "Success"}
            return jsonify(message), 200
        return {"message" : "Fail"}, 400
