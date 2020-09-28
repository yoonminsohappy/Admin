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
        
        # unicode 객체로 변경하기 위해서는 hashpw 함수에 넣기 전에 비밀번호를 encoding 해서 type을 byte로 바꿔준다.
        password            = seller_info['password'].encode('utf-8') 

        # password값을 받아 매칭, 비밀번호를 데이터베이스에 저장해 decoding해줘야 합니다.
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
            'phone_number' : seller_info['phone_number'],
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
            if bcrypt.checkpw( seller_info['password'].encode('utf-8'), seller_data['password'].encode('utf-8')):  #--(1)
                access_token = jwt.encode({'seller_account': seller_account}, self.config['SECRET_KEY'], algorithm = self.config['ALGORITHM']) #--(2)
                # 첫번째 인자로 준 {'seller_account': seller_account} 딕셔너리를 암호화를 하는데 
                # 이때, 두번쨰 인자로 secret_key라는 값과 조합해서 인코드 합니다. 
                # 암호화하는 방식은 3번째 인자값인 algorithm으로 암호화해서 반환한다.
                access_token = access_token.decode('utf-8') #--(3)
                # 그 반환 결과가 바이트 이기 때문에 decode를 통해 다시 문자열로 변환시켜준다.
                return access_token
            raise Exception("Invalid Password")
        raise Exception("Invalid Account")

#셀러 검색 기능
    def search_seller_list(self, conn, search_keyword, search_value):
        #각각의 keyword별로 쿼리문에 적용할 별칭과 컬럼에 맞춰서 변경
        sellers_keywords = ['id','seller_account','english_name','korean_name','registered_product_count','register_date'] #sellers의 검색 조건
        managers_keywords = ['manager_name','manager_phone_number','manager_email'] #seller_manager_tables의 검색 조건
        
        #각각에 해당하는 별칭은 sellers는 s, seller_manager_tables는 m, seller_properties는 p, , seller_statuses는 t
        if search_keyword == 'seller_status': #seller_statuses의 검색 조건
            search_keyword = 't.'+search_keyword
        elif search_keyword == 'seller_property': #seller_properties의 검색 조건
            search_keyword = 'p.'+search_keyword
        elif search_keyword in sellers_keywords:
            search_keyword = 's.'+search_keyword
        elif search_keyword in managers_keywords:
            search_keyword = 'm.'+search_keyword.replace('manager_','')

        result = self.dao.find_search_seller_list(conn, search_keyword, search_value)
        return result
