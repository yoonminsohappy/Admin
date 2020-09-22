from flask import jsonify, request

from flask.views import MethodView 

class SellerSearchView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        search_term = request.args.get('q')
        limit       = request.args.get('limit', '10')
        
        # 쿼리 파라미터 적절한지 확인
        if not search_term or not limit or not limit.isnumeric():
            message = {"message": "CHECK_QUERY_PARAMS"}
            return jsonify(message), 400

        results     = self.service.search_sellers(search_term, limit)
        return jsonify(results), 200

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
























# 작성자: 이지연
# 작성일: 2020.09.22.화
# 로그인 endpoint

# class SellerSignInView(MethodView): 
#     def __init__(self, service):
#         self.service = service 

#     def post(self):
#         data = request.get_json()
        
#         result = self.service.sign_in(data)
#         if result:
#             print(result)
#             message  = {"message" : "Success"}
#             return jsonify(message), 200
#         return {"message" : "Fail"}, 400