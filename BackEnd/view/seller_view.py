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
    @validate_params(
        Param('seller_account',JSON,str,required=True,rules=[Validation_seller_account()]),
        Param('password',JSON,str,required=True,rules=[Validation_password()]),
        Param('phone_number',JSON,str,required=True,rules=[Validation_phone_number()]),
        Param('korean_name',JSON,str,required=True,rules=[Validation_korean_name()]),
        Param('english_name',JSON,str,required=True,rules=[Validation_english_name()]),
        Param('cs_phone',JSON,str,required=True,rules=[Validation_cs_phone()]),
        Param('seller_property',JSON,str,required=True,rules=[Validation_seller_property()])
    )
    def post(self, *args):
        """
        기본 회원가입 API

            Args:
                --sellers table
                    seller_account     : 셀러 아이디 ,
                    english_name       : 영문 셀러명,
                    korean_name        : 셀러명,
                    cs_phone           : 고객센터 전화번호 ,
                    seller_property_id : 셀러 속성 PK(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
                    password           : 패스워드,
                --seller_managers table
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
        """

        try:
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
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            conn.rollback()
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 400
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

    def __init__(self, service):
        self.service = service 

    @catch_exception
    @validate_params(
        Param('seller_account',JSON,str,required=True,rules=[Validation_seller_account()]),
        Param('password',JSON,str,required=True,rules=[Validation_password()]),
    )
    def post(self, *args):
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

        """

        try:
            conn          = connection.get_connection(config.database)
            seller_info   = {
                'seller_account'    :   args[0],
                'password'          :   args[1]
            }
            
            # 로그인 성공 시 access_token 생성 메소드 실행
            access_token  = self.service.sign_in(seller_info,conn)

        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
        #     print(str(e))
            conn.rollback()
            message = {"errno": e.args[0], "errval": e.args[1]}
            # (1054, "Unknown column 'seller_accounts' in 'field list'")
            return jsonify(message), 400
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'UNSUCCESS'}),400
        else:
            conn.commit()
            return jsonify({'access_token':access_token}),200
        finally:
            conn.close() 

# 검색 기능 endpoint
class  SellerSerachView(MethodView):

    def __init__(self, service):
        self.service = service

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
        Param('page',GET, int, required=False, default=1),
        Param('order',GET, str, required=False, default='DESC',rules=[Validation_order()])
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
            2020 - 09 - 27(wldus9503@gmail.com) : 셀러 리스트 초기 생성   
            2002 - 09 - 28(wldus9503@gmail.com) : 수정
                                    ->  유효성 검사 함수를 DAO로 이동
            2020 - 09 - 29(wldus9503@gmail.com) : 셀러 검색 추가, 페이지 네이션 추가 
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
    
    @catch_exception
    @validate_params(
        Param('sellers_id', PATH, str, required=True, default=None), #
        Param('profile_image', JSON, str, required=False, default=None), #
        Param('seller_status', JSON, str, required=False, default=None), #
        Param('seller_property', JSON, str, required=False, default=None,rules=[Validation_seller_property()]), #
        Param('korean_name', JSON, str, required=False, default=None, rules=[Validation_korean_name()]), #
        Param('english_name', JSON, str, required=False, default=None, rules=[Validation_english_name()]), #
        Param('seller_account', JSON, str, required=False, default=None, rules=[Validation_seller_account()]), #
        Param('password', JSON, str, required=False, default=None, rules=[Validation_password()]), #
        Param('background_image', JSON, str, required=False, default=None), #
        Param('simple_description', JSON, str, required=False, default=None), #
        Param('detail_description', JSON, str, required=False, default=None), #
        #담당자정보
        Param('manager_id', JSON, str, required=False, default=None),
        Param('manager_name', JSON, str, required=False, default=None, rules=[Validation_managers_name()]), #
        Param('manager_phone_number', JSON, str, required=False, default=None, rules=[Validation_phone_number()]), #
        Param('manager_email', JSON, str, required=False, default=None, rules=[Validation_managers_email()]),
        #
        Param('cs_phone', JSON, str, required=False, default=None, rules=[Validation_cs_phone()]), #
        Param('zip_code', JSON, str, required=False, default=None), #
        Param('address', JSON, str, required=False, default=None), #
        Param('detail_address', JSON, str, required=False, default=None), #
        Param('open_time', JSON, str, required=False, default=None), #
        Param('close_time', JSON, str, required=False, default=None), #
        #은행
        Param('bank_id', JSON, str, required=False, default=None), #
        Param('bank_name', JSON, str, required=False, default=None, rules=[Validation_bank_name()]),
        #
        Param('account_number', JSON, str, required=False, default=None, rules=[Validation_account_number()]),
        Param('account_name', JSON, str, required=False, default=None, rules=[Validation_account_name()]),
        Param('shipping_information', JSON, str, required=False, default=None, rules=[Validation_shipping_information()]),
        Param('exchange_refund_information', JSON, str, required=False, default=None, rules=[Validation_exchange_refund_information()]),
        Param('model_height', JSON, str, required=False, default=None, rules=[Validation_model_height()]),
        Param('model_top_size', JSON, str, required=False, default=None, rules=[Validation_model_top_size()]),
        Param('model_bottom_size', JSON, str, required=False,default=None, rules=[Validation_model_bottom_size()]),
        Param('model_feet_size', JSON, str, required=False, default=None, rules=[Validation_model_feet_size()]),
        Param('shopping_feedtext', JSON, str, required=False, default=None, rules=[Validation_shopping_feedtext()]),
        Param('registered_product_count', JSON, int, required=False, default=None),
        Param('is_deleted', JSON, bool, required=False, default=False), #
        # Param('modifier_id', JSON, str, required=False, default=None)
    )
    def put(self,*args):
        try:
            conn = connection.get_connection(config.database)

            update_info   = {
                'sellers_id'                    :   args[0],
                'profile_image'                 :   args[1],
                'seller_status'                 :   args[2],
                'seller_property'               :   args[3],
                'korean_name'                   :   args[4],
                'english_name'                  :   args[5],
                'seller_account'                :   args[6],
                'password'                      :   args[7],
                'background_image'              :   args[8],
                'simple_description'            :   args[9],
                'detail_description'            :   args[10],
                #담당자정보
                'manager_id'                    :   args[11],
                'manager_name'                  :   args[12],                                      
                'manager_phone_number'          :   args[13],
                'manager_email'                 :   args[14],
                #
                'cs_phone'                      :   args[15],
                'zip_code'                      :   args[16],
                'address'                       :   args[17],
                'detail_address'                :   args[18],
                'open_time'                     :   args[19],
                'close_time'                    :   args[20],
                #은행
                'bank_id'                       :   args[21],
                'bank_name'                     :   args[22],
                #
                'account_number'                :   args[23],
                'account_name'                  :   args[24],
                'shipping_information'          :   args[25],
                'exchange_refund_information'   :   args[26],
                'model_height'                  :   args[27],
                'model_top_size'                :   args[28],
                'model_bottom_size'             :   args[29],
                'model_feet_size'               :   args[30],
                'shopping_feedtext'             :   args[31],
                'registered_product_count'      :   args[32],
                'is_deleted'                    :   args[33]
            }

            print(update_info)

            results = "aa"
        except Exception as e:
            return jsonify({'message': str(e)}),400
        else:
            return jsonify(results), 200
        finally:
            conn.close()
