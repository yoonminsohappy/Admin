import json, bcrypt

class SellerService:
    def __init__(self, dao, config):
        self.dao = dao 
        self.config = config 

    def search_sellers(self, conn, search_term, limit):
        return self.dao.find_sellers_by_search_term(conn, search_term, limit)


    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint

    def sign_up(self, data):
        seller_property_id = self.dao.get_property_id(data['seller_properties'])
        
        encode_password = bcrypt.hashpw(str(data['password']).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = {
            'seller_account'        : data['seller_account'],
            'password'              : encode_password,
            'seller_property_id'    : seller_property_id,
            'korean_name'           : data['korean_name'],
            'english_name'          : data['english_name'],
            'cs_phone'              : data['cs_phone']
        }

        result = self.dao.insert_seller(user) #seller 인서트 후 마지막 seller의 id값

        manager = {
            'phone_number' : data['seller_phone'],
            'seller_id' : result
        }

        return self.dao.insert_manager(manager)