from flask          import jsonify, request
from flask.views    import MethodView

from connection     import get_connection
from pymysql        import err

#유효성 검사용 모듈 import
from flask_request_validator import (
    GET,
    PATH,
    FORM,
    Param,
    Pattern,
    JSON,
    validate_params
)

from utils.validation import (
    Validation_seller_account,
    Validation_password,
    Validation_phone_number,
    Validation_korean_name,
    Validation_english_name,
    Validation_cs_phone,
    Validation_seller_property,
    Validation_order,
    Validation_managers_name,
    Validation_managers_email,
    Validation_bank_name,
    Validation_account_number,
    Validation_account_name,
    Validation_shipping_information,
    Validation_exchange_refund_information,
    Validation_model_height,
    Validation_model_top_size,
    Validation_model_bottom_size,
    Validation_model_feet_size,
    Validation_shopping_feedtext
)

from utils.decorator import (
    login_decorator,
    catch_exception
)

import config,connection
import traceback

class ProductSellerSearchView(MethodView):
    def __init__(self, service):
        self.service = service

    def get(self):
        """
        상품 등록을 위해 셀러를 검색한다.

        Args:

        Returns:
            200: 
                셀러 정보 딕셔너리 리스트를 JSON으로 리턴
            400: 
                CHECK_QUERY_PARAMS: 쿼리 스트링의 값이 올바르지 않음
            500:
                OperationalError: 데이터베이스 조작 에러
                InternalError   : 데이터베이스 내부 에러

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-20(이충희): 초기 생성
        """
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

# 회원가입 endpoint
class SellerSignUpView(MethodView): 
    
    def __init__(self, service):
        self.service = service #(app->init->view)

    @catch_exception
    #validator에서 오류가 날 경우 500이 아닌 400에러를 반환
    @validate_params(
        #들어온 파라미터들을 유효성 검사한다.
        Param('seller_account',JSON,str,required=True),
        Param('password',JSON,str,required=True),
        Param('phone_number',JSON,str,required=True),
        Param('korean_name',JSON,str,required=True),
        Param('english_name',JSON,str,required=True),
        Param('cs_phone',JSON,str,required=True),
        Param('seller_property',JSON,str,required=True)
    )
    def post(self, *args):
        """
        새로운 셀러를 생성합니다.

            Args:
                    seller_account     : 셀러 아이디 ,
                    english_name       : 영문 셀러명,
                    korean_name        : 셀러명,
                    cs_phone           : 고객센터 전화번호 ,
                    seller_property_id : 셀러 속성 PK(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
                    password           : 패스워드,
                    phone_number       : 담당자 전화번호,
                    seller_id          : 셀러 FK
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
                2020 - 09 - 22(wldus9503@gmail.com) : 초기 생성
                2020 - 09 - 23(wldus9503@gmail.com) : 수정
                                -> view에서 db commit하도록 변경, 에러 처리 추가
                2020 - 09 - 25(wldus9503@gmail.com) : 유효성 검사 추가
                2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경
        """

        try:
            print(request.get_json())
            print(args)
            conn          = connection.get_connection(config.database)   
            seller_info   = {
                'seller_account'    :   args[0],
                'password'          :   args[1],
                'phone_number'      :   args[2],
                'korean_name'       :   args[3],
                'english_name'      :   args[4],
                'cs_phone'          :   args[5],
                'seller_property'   :   args[6]
            }
            sign_up       = self.service.sign_up(seller_info, conn)
        #DB와 관련된 오류
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            traceback.print_exc
            conn.rollback()
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 400
        #그 외 모든 에러들
        except Exception as e:
            conn.rollback()
            return jsonify({'message': str(e)}), 400
        else:
            conn.commit()    
            return jsonify({'message':'SUCCESS'}), 200 
        finally:
            conn.close()  
            
# 로그인 endpoint
class SellerSignInView(MethodView):

    """
        기본 로그인 API

        Args:

            seller_account : 셀러 아이디
            password       : 패스워드
            
        Retruns:
            200, {'access_token':access_token}

            400, {'message': 'UNSUCCESS'}

            400, {"errno": e.args[0], "errval": e.args[1]} : DB와 관련된 오류

            (   #IntegrityError : 데이터베이스의 관계형 무결성에서 발생하는 예외 (외래키 검사 실패, 중복키, 기타)
                #DataError : 0으로 나누기, 범위를 벗어난 숫자 값,기타
                #NotSupportedError : 메서드 또는 데이터베이스 API를 사용한 경우 예외 발생 데이터베이스에서 지원하지 않는 경우( 트랜잭션을 지원하지 않는 연결의 .rollback () 또는 거래가 해제)
                #OperationalError : 데이터베이스와 관련된 오류에 대해 예외, 예기치 않은 연결 해제가 발생하면 데이터 소스 이름이 발견, 트랜잭션을 처리 할 수 ​​없음, 메모리 할당 처리 중 오류
                #InternalError : 데이터베이스가 내부 오류, 예를 들어 커서가 더 이상 유효하지 않습니다. 트랜잭션이 동기화되지 않음 등
            )

            400, {'message':str(e)} : 유효성 검사 오류

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020 - 09 - 23(wldus9503@gmail.com) : 초기 생성
            2020 - 09 - 24(wldus9503@gmail.com) : 수정
            -> view에서 db commit하도록 변경, 에러 처리 추가
            2020 - 09 - 25(wldus9503@gmail.com) : 유효성 검사 추가
            2020 - 09 - 28(wldus9503@gmail.com) : 유효성 검사 customexception -> validationexception 변경
            2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경

    """ 
    def __init__(self, service):
        self.service = service 

    @catch_exception
    @validate_params(
        Param('seller_account',JSON,str,required=True),
        Param('password',JSON,str,required=True)
    )
    def post(self, *args):
       
        try:
            conn          = connection.get_connection(config.database)
            seller_info   = {
                'seller_account'    :   args[0],
                'password'          :   args[1]
            }
            print(request.get_json())
            print(args)
            
            # 로그인 성공 시 access_token 생성 메소드 실행 -> 성공 x : INVALID_USER, INVALID_TOKEN
            access_token  = self.service.sign_in(seller_info,conn)
        #DB 오류
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            traceback.print_exc()
            message = {"errno": e.args[0], "errval": e.args[1]}
            # (1054, "Unknown column 'seller_accounts' in 'field list'")
            return jsonify(message), 400
        #그 외 오류(컬럼명 오타 등)
        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': str(e)}),405
        else:
            return jsonify({'access_token':access_token}),200
        finally:
            conn.close() 

# 검색 기능 endpoint
class  SellerSerachView(MethodView):

    def __init__(self, service):
        self.service = service

    @login_decorator
    @catch_exception
    @validate_params(
        Param('id', GET, str, required=False, default=''),
        Param('seller_account', GET, str, required=False, default=''),
        Param('korean_name', GET, str, required=False, default=''),
        Param('english_name', GET, str, required=False, default=''),
        Param('seller_status', GET, str, required=False, default=''),
        Param('seller_property',GET, str, required=False, default=''),
        Param('manager_name', GET, str, required=False, default=''),
        Param('manager_phone', GET, str, required=False, default=''),
        Param('manager_email', GET, str, required=False,default=''),
        Param('from', GET, str, required=False, default=''),
        Param('to',GET, str, required=False, default=''),
        Param('page',GET, int, required=False, default=1), #현재 페이지
        Param('order',GET, str, required=False, default='DESC',rules=[Validation_order()]) # DAO에서 sql 정렬방식
    )
    def get(self,*args):
        """
        셀러 계정 관리 검색 API

        Args:
            --sellers table
                seller_id                : 셀러 PK
                seller_account           : 셀러 아이디 ,
                english_name             : 영문 셀러명,
                korean_name              : 셀러명,
                registered_product_count : 등록 상품 개수
                register_date            : 등록 일시
            --seller_managers
                name               : 담당자 이름,
                phone_number       : 담당자 전화번호,
                email              : 이메일
            --seller_properties
                name               : 속성 이름(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
            --seller_statuses
                name               : 상태 이름(입점대기, 입점거절, 입점, 휴점, 퇴점 대기, 퇴점)

        Retruns:
            200, results : 해당 검색에 대한 결과

            400, {'message':str(e)} : 잘못된 키워드 오류

        Authors:
            wldus9503@gmail.com(이지연)
        
        History:(
            2020.09.27(이지연) : 셀러 리스트 초기 생성   
            2002.09.28(이지연) : 수정
                                    ->  유효성 검사 함수를 DAO로 이동
            2020.09.29(이지연) : 셀러 검색 추가, 페이지 네이션 추가 
            2020.10.02(이지연) : 모델링 변경 -> 하나의 셀러 테이블을 sellers와 seller_informations으로 나누고 로직 변경

        """

        try:
            conn = connection.get_connection(config.database)

            search_info = {
                'id'                        :   args[0],
                'seller_account'            :   args[1],
                'korean_name'               :   args[2],
                'english_name'              :   args[3],
                'seller_status'             :   args[4],
                'seller_property'           :   args[5],
                'manager_name'              :   args[6],
                'manager_phone'             :   args[7],
                'manager_email'             :   args[8],
                'from'                      :   args[9],
                'to'                        :   args[10],
                'page'                      :   args[11],
                'order'                     :   args[12]
            }
            #from , to - 등록일시 -> 이상/이하 미적용, 구현예정 
            results     = self.service.search_seller_list(conn, search_info)

        except Exception as e:
            return jsonify({'message': str(e)}),400
        else:
            return jsonify(results), 200
        finally:
            conn.close()

#t셀러 수정 기능
class SellerUpdateView(MethodView):

    def __init__(self, service):
        self.service = service
    
    @login_decorator
    @catch_exception
    @validate_params(
        Param('seller_id', PATH, int, required=True, default=None),
        Param('seller_status', FORM , str, required=True, default=None),
        Param('seller_property', FORM, str, required=True, default=None),
        Param('seller_account', FORM, str, required=True, default=None),
        Param('simple_description', FORM, str, required=False, default=None),
        Param('detail_description', FORM, str, required=False, default=None),
        Param('cs_phone', FORM, str, required=True, default=None),
        Param('zip_code', FORM, str, required=False, default=None),
        Param('address', FORM, str, required=False, default=None),
        Param('detail_address', FORM, str, required=False, default=None),
        Param('open_time', FORM, str, required=False, default=None),
        Param('close_time', FORM, str, required=False, default=None),
        Param('bank', FORM, str, required=False, default=None),
        Param('account_number', FORM, str, required=False, default=None),
        Param('account_name', FORM, str, required=False, default=None),
        Param('shipping_information', FORM, str, required=False, default=None),
        Param('exchange_refund_information', FORM, str, required=False, default=None),
        Param('model_height', FORM, str, required=False, default=None),
        Param('model_top_size', FORM, str, required=False, default=None),
        Param('model_bottom_size', FORM, str, required=False, default=None),
        Param('model_feet_size', FORM, str, required=False, default=None),
        Param('shopping_feedtext', FORM, str, required=False, default=None),
        Param('password', FORM, str, required=False, default=None),
        Param('manager_info[0]', FORM, dict, required=True, default=None),
        Param('manager_info[1]', FORM, dict, required=False, default=None),
        Param('manager_info[2]', FORM, dict, required=False, default=None)
    )
    #Form으로 한 이유: 이미지 파일과 json데이터를 한꺼번에 요청하기 위해서

    def put(self,*args):
        try:    
            conn = connection.get_connection(config.database)

            update_info   = {
                'seller_id'                   : args[0],
                'seller_status'               : args[1],
                'seller_property'             : args[2],
                'seller_account'              : args[3],
                'simple_description'          : args[4],
                'detail_description'          : args[5],
                'cs_phone'                    : args[6],
                'zip_code'                    : args[7],
                'address'                     : args[8],
                'detail_address'              : args[9],
                'open_time'                   : args[10],
                'close_time'                  : args[11],
                'bank'                        : args[12],
                'account_number'              : args[13],
                'account_name'                : args[14],
                'shipping_information'        : args[15],
                'exchange_refund_information' : args[16],
                'model_height'                : args[17],
                'model_top_size'              : args[18],
                'model_bottom_size'           : args[19],
                'model_feet_size'             : args[20],
                'shopping_feedtext'           : args[21],
                'password'                    : args[22],
                'manager_infos'               : None
            }

            #매니저정보 1개 이상 최대 3개를 받음.
            manager_infos = []

            #None이 아닌 매니저 정보는 리스트에 담는다(args-23,24,25까지)
            for i in range(23,26):
                if args[i] != None:
                    manager_infos.append(args[i])
            #update_info에 리스트를 담는다.
            update_info['manager_infos'] = manager_infos

            #데코레이터로 부터 저장한 요청자의 id값 = 수정자의 id
            modifier_user = request.user
            
            #프로필 이미지 및 배경화면 이미지 값 받아오기
            profile_image = request.files.get('profile_image', None)
            background_image = request.files.get('background_image', None)
            
            results = self.service.update_seller(conn, update_info,profile_image,background_image,modifier_user)
        except Exception as e:
            conn.rollback()
            return jsonify({'message': str(e)}),400
        else:
            conn.commit()
            return jsonify(results), 200
        finally:
            conn.close()

    @catch_exception
    @validate_params(
        Param('seller_id', PATH, str, required=True, default=None)
    )
    def get(self,*args):

        try: 
            #db연결
            conn            = get_connection(config.database)
            #seller_id를 인자로 갖 고온다.
            seller_id       = args[0]
            #service에서 넘겨준 값을 results변수에 담는다.
            results          = self.service.detail_seller(conn, seller_id)
        
        #예외처리
        except Exception as e:

            return jsonify({'message':str(e)}), 400
        else:
            return jsonify(results), 200
        finally:
            conn.close()