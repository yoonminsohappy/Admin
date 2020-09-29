import json, bcrypt, jwt
from flask_paginate import Pagination, get_page_args

class SellerService:
    def __init__(self, dao, config):
        self.dao    = dao 
        self.config = config 

    def search_sellers(self, conn, search_term, limit):
        """
        상품 등록을 위해 셀러를 검색한다.

        Args:
            conn       : 데이터베이스 커넥션 객체
            search_term: 검색어
            limit      : 몇 개의 row를 가져올지 정하는 수

        Returns:
            results: 셀러 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"                : 셀러 아이디,
                        "korean_name"       : 셀러 한글 이름,
                        "profile_image"     : 프로파일 이미지,
                        "seller_property_id": 샐러 속성 아이디
                    },
                    ...
                ] 

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-20(이충희): 초기 생성
        """
        return self.dao.find_sellers_by_search_term(conn, search_term, limit)

    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint

    def sign_up(self, seller_info, db):
        seller_property_id  = self.dao.get_property_id(seller_info['seller_property'],db)
        
        password            = seller_info['password'].encode('utf-8') 
        password_crypt      = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8') 

        if seller_info is None:
            raise Exception("INVALID_PARAMETER")

        seller = {
            'seller_account'        : seller_info['seller_account'],
            'password'              : password_crypt,
            'seller_property_id'    : seller_property_id['id'],
            'korean_name'           : seller_info['korean_name'],
            'english_name'          : seller_info['english_name'],
            'cs_phone'              : seller_info['cs_phone']
        }
        result = self.dao.insert_seller(seller,db)        

        if result is None:
            raise Exception("INVALID_PARAMETER")

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
                
                access_token = access_token.decode('utf-8') #--(3) 그 반환 결과가 바이트 이기 때문에 decode를 통해 다시 문자열로 변환시켜준다.
                return access_token
            raise Exception("Invalid Password")
        raise Exception("Invalid Account")

#셀러 검색, 전체리스트
    def search_seller_list(self, conn, search_info):
        results = {}

        if search_info is None:
            raise Exception("INVALID_PARAMETER")

        total_count = self.dao.find_search_total_seller_list(conn, search_info)

        total_page  = int(total_count/10)

        seller_list = []
        
        if search_info['page'] <= total_page:
            seller_list = self.dao.find_search_seller_list(conn, search_info)

        results['seller_list'] = seller_list
        results['total_page']  = int(total_count/10)
        results['total_count'] = total_count
        
        return results