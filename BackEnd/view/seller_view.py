from flask          import jsonify, request
from flask.views    import MethodView

from connection     import get_connection
from pymysql        import err

from utils.custom_error import CustomException
from utils.validation import (
    validation_seller_account,
    validation_password,
    validation_phone_number,
    validation_korean_name,
    validation_english_name,
    validation_cs_phone,
    validation_search_keyword
)
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



# 회원가입 endpoint
class SellerSignUpView(MethodView):  # 특정 메서드에 요청을 전달,메서드를 구현하면 요청에 응답 
    
    #  기본 회원가입 API

    #     Args:
    #         --sellers table
    #             seller_account     : 셀러 아이디 ,
    #             english_name       : 영문 셀러명,
    #             korean_name        : 셀러명,
    #             cs_phone           : 고객센터 전화번호 ,
    #             seller_property_id : 셀러 속성 PK(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
    #             password           : 패스워드,
    #         --seller_managers table
    #             phone_number       : 담당자 전화번호,
    #             seller_id          : 셀러 FK
    #     Retruns:
    #         200, {'message': 'SUCCESS'} : 회원가입 성공

    #         400, {'message':str(e)} : 회원가입 실패, 유효성 검사 오류

    #         400, {"errno": e.args[0], "errval": e.args[1]} : DB와 관련된 오류

    #         (  
    #             IntegrityError : 데이터베이스의 관계형 무결성에서 발생하는 예외 (외래키 검사 실패, 중복키, 기타)
    #             DataError : 0으로 나누기, 범위를 벗어난 숫자 값,기타
    #             NotSupportedError : 메서드 또는 데이터베이스 API를 사용한 경우 예외 발생 데이터베이스에서 지원하지 않는 경우( 트랜잭션을 지원하지 않는 연결의 .rollback () 또는 거래가 해제)
    #             OperationalError : 데이터베이스와 관련된 오류에 대해 예외, 예기치 않은 연결 해제가 발생하면 데이터 소스 이름이 발견, 트랜잭션을 처리 할 수 ​​없음, 메모리 할당 처리 중 오류
    #             InternalError : 데이터베이스가 내부 오류, 예를 들어 커서가 더 이상 유효하지 않습니다. 트랜잭션이 동기화되지 않음 등
    #         )

    #     Authors:
    #         wldus9503@gmail.com(이지연)
        
    #     History:
    #         2020 - 09 - 22(wldus9503@gmail.com) : 초기 생성
    #         2020 - 09 - 23(wldus9503@gmail.com) : 수정
    #                         -> view에서 db commit하도록 변경, 에러 처리 추가
    #         2020 - 09 - 25(wldus9503@gmail.com) : 유효성 검사 추가
    
    def __init__(self, service):
        self.service = service #메소드별로 사용할 수 있도록 해당 service변수에 service를 넣어줌 (app->init->view)

    def post(self):

        try:
            conn          = connection.get_connection(config.database)
            #flask 에서 기본적으로 제공하는 get_json 함수를 사용해서 post 방식으로 보내는 json 데이터 처리법을 정리
            seller_info   = request.get_json() 

            #유효성 검사
            validation_seller_account(seller_info['seller_account'])
            validation_password(seller_info['password'])
            validation_phone_number(seller_info['phone_number'])
            validation_korean_name(seller_info['korean_name'])
            validation_english_name(seller_info['english_name'])
            validation_cs_phone(seller_info['cs_phone'])

            sign_up       = self.service.sign_up(seller_info, conn)

        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
            message = {"errno": e.args[0], "errval": e.args[1]}
            return jsonify(message), 400
        except Exception as e:
            conn.rollback()
            return jsonify({'message':str(e)}), 400
        else:
            conn.commit()    
            return jsonify({'message':'SUCCESS'}), 200 
        finally:
            conn.close()  
            
# 로그인 endpoint
class SellerSignInView(MethodView): 
 
        # 기본 로그인 API

        # Args:

        #     seller_account : 셀러 아이디
        #     password       : 패스워드
            
        # Retruns:
        #     200, {'access_token':access_token}

        #     400, {'message': 'UNSUCCESS'}

        #     400, {"errno": e.args[0], "errval": e.args[1]} : DB와 관련된 오류

        #     (   #IntegrityError : 데이터베이스의 관계형 무결성에서 발생하는 예외 (외래키 검사 실패, 중복키, 기타)
        #         #DataError : 0으로 나누기, 범위를 벗어난 숫자 값,기타
        #         #NotSupportedError : 메서드 또는 데이터베이스 API를 사용한 경우 예외 발생 데이터베이스에서 지원하지 않는 경우( 트랜잭션을 지원하지 않는 연결의 .rollback () 또는 거래가 해제)
        #         #OperationalError : 데이터베이스와 관련된 오류에 대해 예외, 예기치 않은 연결 해제가 발생하면 데이터 소스 이름이 발견, 트랜잭션을 처리 할 수 ​​없음, 메모리 할당 처리 중 오류
        #         #InternalError : 데이터베이스가 내부 오류, 예를 들어 커서가 더 이상 유효하지 않습니다. 트랜잭션이 동기화되지 않음 등
        #     )

        #     400, {'message':str(e)} : 유효성 검사 오류

        # Authors:
        #     wldus9503@gmail.com(이지연)
        
        # History:(
        #     2020 - 09 - 23(wldus9503@gmail.com) : 초기 생성
        #     2020 - 09 - 24(wldus9503@gmail.com) : 수정
        #     -> view에서 db commit하도록 변경, 에러 처리 추가
        #     2020 - 09 - 25(wldus9503@gmail.com) : 유효성 검사 추가

    def __init__(self, service):
        self.service = service 

    def post(self):

        try:
            conn          = connection.get_connection(config.database)
            seller_info   = request.get_json()
            
            validation_seller_account(seller_info['seller_account'])
            validation_password(seller_info['password'])
            
            # 로그인 성공 시 access_token 생성 메소드 실행
            access_token  = self.service.sign_in(seller_info,conn)
        except CustomException as e:
            return jsonify({'message':str(e)}),400
        except (err.IntegrityError,err.DataError, err.NotSupportedError, err.OperationalError,err.InternalError) as e:
        #     print(str(e))
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

        # 셀러 계정 관리 검색 API

        # Args:
        #     --sellers table
        #         seller_id                : 셀러 PK
        #         seller_account           : 셀러 아이디 ,
        #         english_name             : 영문 셀러명,
        #         korean_name              : 셀러명,
        #         registered_product_count : 등록 상품 개수
        #         register_date            : 등록 일시
        #     --seller_managers
        #         name               : 담당자 이름,
        #         phone_number       : 담당자 전화번호,
        #         email              : 이메일
        #     --seller_properties
        #         name               : 속성 이름(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
        #     --seller_statuses
        #         name               : 상태 이름(입점대기, 입점거절, 입점, 휴점, 퇴점 대기, 퇴점)

        # Retruns:
        #     200, results : 해당 검색에 대한 결과

        #     400, {'message':str(e)} : 잘못된 키워드 오류

        # Authors:
        #     wldus9503@gmail.com(이지연)
        
        # History:(
        #     2020 - 09 - 27(wldus9503@gmail.com) : 초기 생성

    def __init__(self, service):
        self.service = service

    def get(self):

        try:
            conn = connection.get_connection(config.database)
            
            #검색 키워드값
            search_keyword = request.args.get('keyword')
            #올바른 검색 키워드인지 검사,에러처리
            validation_search_keyword(search_keyword) 
            #검색 내용값
            search_value   = request.args.get('value')

            results     = self.service.search_seller_list(conn, search_keyword, search_value)
        except Exception as e:
            conn.rollback()
            return jsonify({'message': str(e)}),400
        else:
            return jsonify(results), 200
        finally:
            conn.close()