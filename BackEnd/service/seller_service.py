import json, bcrypt, jwt, datetime
import boto3
import uuid
from flask          import jsonify
from flask_paginate import Pagination, get_page_args

from pyexcel_xls    import save_data
from werkzeug.utils import secure_filename

class SellerService:
    def __init__(self, dao, config):
        self.dao    = dao 
        self.config = config
        self.s3     = boto3.client(
            "s3",
            aws_access_key_id     = config['S3_ACCESS_KEY_SELLER'],
            aws_secret_access_key = config['S3_SECRET_KEY_SELLER']
        )

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


    # 회원가입 endpoint
    def sign_up(self, seller_info, conn):

        """
        새로운 셀러를 생성합니다.
            Args:
                seller_info : view에서 7개의 파라미터들 딕셔너리 형태로 넣어준 변수
            Retruns:
                200, {'message': 'SUCCESS'} : 회원가입 성공
                400, {'message':str(e)} : 회원가입 실패, 유효성 검사 오류
                400, {"errno": e.args[0], "errval": e.args[1]} : DB와 관련된 오류
                (  
                    IntegrityError : 데이터베이스의 관계형 무결성에서 발생하는 예외 (외래키 검사 실패, 중복키, 기타)
                    DataError : 0으로 나누기, 범위를 벗어난 숫자 값,기타
                    NotSupportedError : 메서드 또는 데이터베이스 API를 사용한 경우 예외 발생 데이터베이스에서 지원하지 않는 경우( 트랜잭션을 지원하지 않는 연결의 .rollback () 또는 거래가 해제)
                    OperationalError : 데이터베이스와 관련된 오류에 대해 예외, 예기치 않은 연결 해제가 발생하면 데이터 소스 이름이 발견, 트랜잭션을 처리 할 수 ​​없음, 메모리 할당 처리 중 오류
                    InternalError : 데이터베이스가 내부 오류, 예를 들어 커서가 더 이상 유효하지 않습니다. 트랜잭션이 동기화되지 않음 등
                )
            Authors:
                wldus9503@gmail.com(이지연)
            
            History:
                2020.09.22(이지연)) : 초기 생성
                2020.09.23(이지연)) : 수정
                                -> view에서 db commit하도록 변경, 에러 처리 추가
                2020.09.25(이지연)) : 유효성 검사 추가
                2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
                2020.10.07(이지연) : 회원가입할 시 셀러 계정아이디, 셀러 cs_phone, manager_phone unique처리 추가
        """

        #유니크 검사 (seller_account, email, cs_phone, phone_number)
        #seller_account
        if self.dao.unique_seller_account(conn, seller_info['seller_account']): #0이 아니면 if문 조건 참, 0이면 거짓
            raise Exception("UNIQUE_SELLER_ACCOUNT") #참인경우는 즉, 동일한 아이디에 대한 데이터가 있다
        
        #seller_property_id
        seller_property_id  = self.dao.get_property_id(conn,seller_info['seller_property'])
        if seller_property_id is None:
            raise Exception("INVALID_PARAMETER")

        #password
        password            = seller_info['password'].encode() 
        password_crypt      = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')

        if seller_info is None:
            raise Exception("INVALID_PARAMETER")
        
        #sellers테이블에 넣은 id값
        pk_seller_id = self.dao.insert_sellers(conn) #sellers의 id(pk)값을 의미
        if pk_seller_id is None:
            raise Exception("INVALID_PARAMETER")

        #cs_phone
        if self.dao.unique_cs_phone(conn, seller_info['cs_phone']):
            raise Exception("UNIQUE_SELLER_CS_PHONE")

        seller = {
            'seller_id'             : pk_seller_id,
            'seller_account'        : seller_info['seller_account'],
            'password'              : password_crypt,
            'seller_property_id'    : seller_property_id['id'],
            'korean_name'           : seller_info['korean_name'],
            'english_name'          : seller_info['english_name'],
            'cs_phone'              : seller_info['cs_phone'],
            'modifier_id'           : pk_seller_id
        }
        
        result = self.dao.insert_seller_infomation(seller, conn)
        
        if result is None:
            raise Exception("INVALID_PARAMETER")

        result_seller = self.dao.find_seller_infomation(conn, result)
        
        #변경이력 기록
        if self.dao.insert_modification_history(conn, result_seller) is None:
            raise Exception("INVALID_PARAMETER1")

        if self.dao.unique_manager_phone(conn, seller_info['phone_number']):
            raise Exception("UNIQUE_SELLER_MANAGER_PHONE")

        manager = {
            'manager_phone'     : seller_info['phone_number'],
            'seller_id'         : pk_seller_id,
            'manager_name'      : 'NoData', #이유:회원가입시 담당자 관련 정보는 전화번호만 받지만 
            'manager_email'     : 'NoData'  #컬럼을 null값으로 두고 검색기능쪽에서 like를 통해서 "%%"로 전체검색을 하더라도 null값이여서 인식이 안되기 때문 
        }                                   # select * from seller_informations where seller_account like "%%"; 
                                            # SQL문 LIKE 에서 _ 와 % :

        if manager is None:
            raise Exception("INVALID_PARAMETER")

        return self.dao.insert_manager(manager,conn)

    # 로그인 endpoint
    def sign_in(self, seller_info, conn):
        seller_account = seller_info['seller_account']
        
        #DB에 실제 아이디값이 존재하는지 확인 위해
        seller_data    = self.dao.select_seller(seller_account, conn)
        
        if seller_data is not None:
            if bcrypt.checkpw( seller_info['password'].encode('utf-8'), seller_data['password'].encode('utf-8')):
                access_token = jwt.encode({'seller_id': seller_data['seller_id']}, self.config['SECRET_KEY'], algorithm = self.config['ALGORITHM']) 

                # 첫번째 인자로 준 {'seller_account': seller_account} 딕셔너리를 암호화를 하는데 #seller_id 즉, sellers pk 로 암호화
                # 이때, 두번쨰 인자로 secret_key라는 값과 조합해서 인코드 합니다. 
                # 암호화하는 방식은 3번째 인자값인 algorithm으로 암호화해서 반환한다.
                
                access_token = access_token.decode('utf-8') #--(3) 그 반환 결과가 바이트 이기 때문에 decode를 통해 다시 문자열로 변환시켜준다.
 
                return access_token
            raise Exception("Invalid Password")
        raise Exception("Invalid Account")

    #셀러 검색, 전체리스트
    def search_seller_list(self, conn, search_info):
        results = {}

        # 과거 데이터 pk값들 추출하기
        #past_sellers_pk = self.dao.find_past_sellers(conn)

        if search_info is None:
            raise Exception("INVALID_PARAMETER")
        
        #조건에 맞는 총 개수 구함
        total_count = self.dao.find_search_total_seller_list(conn, search_info)
        #총 페이지 개수 구함
        total_page  = int(total_count/search_info['per_page'])+1
        
        #한 ID당 하나의 리스트 값들을 넣기 위해서 
        seller_list = []
        
        #현재 페이지가 전체페이지보다 작거나 같으면
        if search_info['page'] <= total_page:
            temp = []
            #검색결과 리스트
            result_list = self.dao.find_search_seller_list(conn, search_info) 
            for result in result_list: #리스트 돌면서
                if result['id'] not in temp: #temp리스트에 id값이 존재하지 않는 경우만 append 즉, 중복없이 하나씩만 넣기
                    temp.append(result['id']) #temp에 id값 넣기
                    seller_list.append(result) #반환용 seller_list에 검색결과 row하나씩 넣기

        results['seller_list'] = seller_list
        results['total_page']  = total_page
        results['total_count'] = total_count
        
        return results

    #셀러계정관리- 수정/조회페이지
    def update_seller(self, conn, update_info, profile_image, background_image, modifier_user):
        #수정자가 자신이거나 mater인지 검사
        
        if modifier_user['seller_id'] != update_info['seller_id'] and modifier_user['is_master'] == 0:
            raise Exception("UNAUTHORIZATION")
        
        # unique
        if modifier_user['seller_account'] != update_info['seller_account'] and self.dao.unique_seller_account(conn, update_info['seller_account']): #0이 아니면 if문 조건 참, 0이면 거짓
            raise Exception("UNIQUE_SELLER_ACCOUNT") #참인경우는 즉, 동일한 아이디에 대한 데이터가 있다

        if modifier_user['cs_phone'] != update_info['cs_phone'] and self.dao.unique_cs_phone(conn, update_info['cs_phone']):
            raise Exception("UNIQUE_SELLER_CS_PHONE")

        #현재 데이터
        past_seller_info = self.dao.find_seller(conn, update_info['seller_id'])
        
        #과거 데이터 삽입
        if self.dao.insert_past_seller_information(conn,past_seller_info) is None:
            raise Exception("INVALID PARAMETER")
        
        updated_info = {}
        
        for key, value in update_info.items():
            if value != None:
                 #셀러 속성 id값 가져온 후 updated_info에 추가
                if key == 'seller_property':
                    seller_property_id = self.dao.get_property_id(conn,value)
                    if seller_property_id is None:
                        raise Exception("INVALID PROPERTY")
                    updated_info['seller_property_id'] = seller_property_id['id']
                #셀러 상태 id값 가져온 후 updated_info에 추가
                elif key == 'seller_status': 
                    seller_status_id = self.dao.get_status_id(conn,value)
                    if seller_status_id is None:
                        raise Exception("INVALID STATUS")
                    updated_info['seller_status_id'] = seller_status_id['id']
                #은행 id값 가져온 후 updated_info에 추가
                elif key == 'bank': 
                    bank_id = self.dao.get_bank_id(conn,value)
                    if bank_id is None:
                        raise Exception("INVALID BANK")
                    updated_info['bank_id'] = bank_id['id']
                #패스워드 변경시 암호화 후 updated_info에 추가
                elif key == 'password':
                    password            = update_info['password'].encode('utf-8') 
                    password_crypt      = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')
                    updated_info['password'] = password_crypt
                elif key != 'manager_infos':
                    updated_info[key] = value

        #profile_image 처리
        if profile_image != None:
            #파일명 안전 검사
            filename = secure_filename(profile_image.filename)
            #S3에 넣을 파일명 지정 seller_id + 이미지종류 + 실제 파일명
            filename = str(updated_info["seller_id"])+"_profile_image_"+filename
            #s3업로드 결과 url 반환
            updated_info['profile_image'] = self.save_seller_image(profile_image,filename)
        
        #background_image 처리
        if background_image != None:
            #파일명 안전 검사
            filename = secure_filename(background_image.filename)
            #S3에 넣을 파일명 지정 seller_id + 이미지종류 + 실제 파일명
            filename = str(updated_info["seller_id"])+"_background_image_"+filename
            #s3업로드 결과 url 반환
            updated_info['background_image'] = self.save_seller_image(background_image,filename)
            
        #수정할 데이터로 update (최신)
        results = self.dao.update_seller_information(conn, updated_info, past_seller_info['id'])
        
        #셀러 상태 변경시 상태 변경 이력 추가
        if past_seller_info['seller_status_id'] != updated_info['seller_status_id']:
            print("asd")
            seller_info = {
                'seller_id'         : updated_info['seller_id'],                
                'created_at'        : datetime.datetime.now(),                
                'seller_status_id'  : updated_info['seller_status_id'],
                'modifier_id'       : modifier_user['seller_id'],     
                }
            #datetime.datetime : 날짜와 시각의 정보를 담음
            re = self.dao.insert_modification_history(conn, seller_info)
            
        # 매니저 처리
        self.dao.delete_managers(conn,updated_info['seller_id']) #현재 등록된 모든 manager를 삭제
        for manager in update_info['manager_infos']: #리스트형으로 받은 최대 3명의 매니저를 insert
            
            #담당자 핸드폰 유니크 검사
            if self.dao.unique_manager_phone(conn, manager['manager_phone']):
                raise Exception("UNIQUE_SELLER_MANAGER_PHONE")
            #담당자 이메일 유니크 검사
            if self.dao.unique_manager_email(conn, manager['manager_email']):
                raise Exception("UNIQUE_SELLER_MANAGER_EMAIL")

            manager['seller_id'] = updated_info['seller_id']
            self.dao.insert_manager(manager,conn)

        return "수정 완료" if results > 0 else "수정 실패"

    # s3에 이미지 파일 업로드
    def save_seller_image(self, image, filename):
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET_SELLER'],
            filename
        )
        #올린 이미지 파일의 url 반환
        image_url = f"{self.config['S3_BUCKET_URL_SELLER']}{filename}"

        return image_url

    #셀러 수정 페이지
    def detail_seller(self, conn, seller_id):
        """
        셀러 수정 페이지를 위해 셀러의 정보를 가져온다.
        Args:
            conn       : 데이터베이스 커넥션 객체
            seller_id  : 해당 셀러 id에 해당하는 정보를 갖고 오기 위함
        Returns:
            results: 셀러 정보를 담은 딕셔너리 리스트
                "manager":[
                                {
                                    "email": "담당자 이메일",
                                    "name":  "담당자 이름",
                                    "phone_number": "담당자 전화번호"
                                },
                            ...(최대3까지)
                "seller":{
                            "account_name": "계좌명",
                            "account_number": "계좌번호",
                            "address": "셀러 주소",
                            "background_image": "셀러페이지배경이미지url",
                            "bank_id": 은행 아이디,
                            "close_time": "운영 마감시간",
                            "created_at": "선분이력시작일자",
                            "cs_phone": "고객센터 전화번호",
                            "detail_address": "상세 주소",
                            "detail_description": "상세 소개",
                            "english_name": "셀러 영문 이름",
                            "exchange_refund_information": "교환/환불정보",
                            "expired_at": "선분이력종료일자",
                            "id": 셀러 아이디 PK,
                            "korean_name": "셀러 한글 이름",
                            "model_bottom_size": "모델 하의 사이즈",
                            "model_feet_size": "모델 신발 사이즈",
                            "model_height": "모델 키",
                            "model_top_size": "모델 상의 사이즈",
                            "modifier_id": 수정자 아이디(default:null),
                            "open_time": "운영시작시간",
                            "password": "패스워드",
                            "profile_image": "프로필 이미지 url",
                            "seller_account": "셀러 계정 id",
                            "seller_id": 셀러 고유 아이디,
                            "seller_property_id": 셀러 속성 아이디,
                            "seller_status_id": 셀러 상태 아이디,
                            "shipping_information": "배송정보",
                            "shopping_feedtext": "쇼핑피드텍스트",
                            "simple_description": "한줄 소개",
                            "zip_code": "우편번호"
                            },
                "seller_modification":[
                    [1, "2020-10-03 22:25:26", "입점대기", "testa1234_1" ],
                     [1, "2020-10-03 22:25:26",…]
              }] 
        Author:
            이지연(wldus9503@@gmail.com)
        History:
            2020-10-04(이지연): 초기 생성
        """

        #딕셔너리로 결과를 담을 변수 생성
        results = {}
        print('1')
        #seller테이블에 해당하는 컬럼값
        seller = self.dao.find_detail_seller(conn, seller_id) 
        if seller is None:
            raise Exception("INVALID_PARAMETER")
        print('2')
        #manager테이블에 해당하는 컬럼값
        manager = self.dao.find_detail_manager(conn, seller_id)
        if manager is None:
            raise Exception("INVALID_PARAMETER")
        print('3')
        #변경이력 테이블에 해당하는 컬럼값
        seller_modification = self.dao.find_detail_seller_modification(conn, seller_id)
        if seller_modification is None:
            raise Exception("INVALID_PARAMETER")
        print('4')

        #딕셔너리로 값을 넣어준다.
        results['seller'] = seller
        results['manager'] = manager
        results['seller_modification'] = seller_modification
        
        return results

    #엑셀 다운로드
    def make_excel_file(self, conn, search_info):
        
        results = {}

        if search_info is None:
            raise Exception("INVALID_PARAMETER")

        seller_list = []
        temp = []
        #검색결과 리스트
        result_list = self.dao.find_search_seller_list_excel(conn, search_info)

        for result in result_list: #리스트 돌면서
            if result['id'] not in temp: #temp리스트에 id값이 존재하지 않는 경우만 append 즉, 중복없이 하나씩만 넣기
                temp.append(result['id']) #temp에 id값 넣기
                seller_list.append(result) #반환용 seller_list에 검색결과 row하나씩 넣기

        #엑셀 상단 컬럼명
        data = [['번호','셀러아이디','영문이름','한글이름', '담당자이름','셀러상태','담당자연락처','담당자이메일','셀러속성','상품개수','등록일시']]

        #중복 제거한 seller_list를 순선대로 data에 리스트 형으로 append
        for i, item in enumerate(seller_list):
            data.append([
                item['id'],
                item['seller_account'],
                item['english_name'],
                item['korean_name'],
                item['manager_name'],
                item['seller_status'],
                item['manager_phone_number'],
                item['manager_email'],
                item['seller_property'],
                item['registered_product_count'],
                item['register_date']
            ])
        
        #data라는 엑셀에 넣을 데이터를 만들어낸 후
        #directory는 "temp/" 라는 폴더로 지정
        directory = "temp/"
        #uuid.uuid4()를 통해서 겹치지않게하는 문자열로 .xls파일을 만들어 냄
        filename = f"{str(uuid.uuid4())}.xls"

        #엑셀 생성시에는 pyexcel_xls의 save_data라는 함수를 이용하여 생성하고
        #디렉토리, 파일명, "셀러리스트엑셀_브랜디.xls"(고정값)을 return
        save_data(directory + filename, {"data": data})

        return directory, filename, "셀러리스트엑셀_브랜디.xls"

