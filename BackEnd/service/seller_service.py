import json, bcrypt, jwt

class SellerService:
    def __init__(self, dao, config):
        self.dao    = dao 
        self.config = config 

    def search_sellers(self, conn, search_term, limit):
        return self.dao.find_sellers_by_search_term(conn, search_term, limit)

    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint

    def sign_up(self, seller_info, db):
        seller_property_id  = self.dao.get_property_id(seller_info['seller_properties'],db)
        password            = seller_info['password'].encode()
        password_crypt      = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')

        seller = {
            'seller_account'        : seller_info['seller_account'],
            'password'              : password_crypt,
            'seller_property_id'    : seller_property_id['id'],
            'korean_name'           : seller_info['korean_name'],
            'english_name'          : seller_info['english_name'],
            'cs_phone'              : seller_info['cs_phone']
        }

        result = self.dao.insert_seller(seller,db)
        
        manager = {
            'phone_number' : seller_info['seller_phone'],
            'seller_id'    : result
        }   

        return self.dao.insert_manager(manager,db)

    # 작성자: 이지연
    # 작성일: 2020.09.23.수
    # 로그인 endpoint

    def sign_in(self, seller_info, db):
        seller_account = seller_info['seller_account']
        
        seller_data    = self.dao.select_seller(seller_account, db)
        if seller_data is not None:
            if bcrypt.checkpw( seller_info['password'].encode('utf-8'), seller_data['password'].encode('utf-8')):
                access_token = jwt.encode({'seller_account': seller_account}, self.config['SECRET_KEY'], algorithm = self.config['ALGORITHM'])
                access_token = access_token.decode('utf-8')
                return access_token
            raise Exception("Invalid Password")
        raise Exception("Invalid Account")