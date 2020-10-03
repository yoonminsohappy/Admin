import re
import datetime

from flask_request_validator import AbstractRule
from exceptions import ValidationError
"""
        validation API

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
                -- order               : sql order기능 위한 변수


            Retruns:
                errors, 오류 반환, 딕셔너리 형태, api이용

            Authors:
                wldus9503@gmail.com(이지연)
            
            History:
                2020 - 09 - 25(wldus9503@gmail.com) : 유효성 검사
                2020 - 09 - 28(wldus9503@gmail.com) : 유효성 검사 customexception -> validationexception 변경
                2020 - 09 - 29(wldus9503@gmail.com) : 클래스 Validation_order 추가, DB ORDER기능 위한것
                2020 - 09 - 30(wldus9503@gmail.com) : 수정 페이지를 위한 유효성 검사 추가
"""

#AbstractRule : 우선 순위를 보통으로 설정하고 상태를 활성으로 설정하는 기본 생성자

class Validation_seller_account(AbstractRule):

    def validate(self, value):
        errors = []
        seller_account_reg = r"^[0-9a-zA-Z][0-9a-zA-Z_-]{5,20}$"
        regex  = re.compile(seller_account_reg)

        if not regex.match(value):
            errors.append('아이디는 5~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다.')
        return errors

class Validation_password(AbstractRule):
    
    def validate(self, value):
        errors = []
        password_reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$"
        regex        = re.compile(password_reg)
        
        if not regex.match(value):
            errors.append('8~20글자의  영문대소문자, 숫자, 특수문자 조합을 사용해주세요.')
        return errors

class Validation_phone_number(AbstractRule):
    
    def validate(self, value):
        errors = []
        phone_number_reg = re.compile(r'\d{3}-\d{3,4}-\d{4}')
        regex        = re.compile(phone_number_reg)

        if not regex.match(value):
            errors.append('올바른 전화번호 형식으로 작성해주세요.')
        return errors

class Validation_korean_name(AbstractRule):
    
    def validate(self, value):
        errors = []
        korean_name_reg = re.compile(r"[ᄀ-힣a-zA-Z0-9]")
        regex       = re.compile(korean_name_reg)
        
        if not regex.match(value):
            errors.append('한글,영문,숫자만 입력해주세요.')
        return errors

class Validation_english_name(AbstractRule):
    
    def validate(self, value):
        errors = []
        english_name_reg = re.compile(r"[a-z]")
        regex  = re.compile(english_name_reg)

        if not regex.match(value):
            errors.append('셀러 영문명은 소문자만 입력가능합니다.')
        return errors

class Validation_cs_phone(AbstractRule):
    
    def validate(self, value):
        errors = []
        cs_phone_reg = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')
        regex    = re.compile(cs_phone_reg)

        if not regex.match(value):
            errors.append('고객센터 전화번호는 숫자와 하이픈만 입력가능합니다.')
        return errors

class Validation_seller_property(AbstractRule):

    def validate(self, value):
        errors = []
        seller_property_reg = ['쇼핑몰','마켓','로드샵','디자이너브랜드','제너럴브랜드','내셔널브랜드','뷰티']
        
        if value not in seller_property_reg:
            errors.append('잘못된 셀러 속성입니다.')
        return errors

class Validation_order(AbstractRule):

    def validate(self, value):
        errors = []
        order_reg = [
            'asc', 
            'desc',
            'ASC',
            'DESC'
            ]
        if value not in order_reg:
            errors.append('잘못된 sql 구문입니다.')
        return errors

def validate_products_limit(limit):
    result = None
    limits = [10, 20, 50]

    if limit.isnumeric():
        if int(limit) not in limits:
            raise ValidationError("LIMIT_MUST_BE_IN_[10, 20, 50]")
        result = int(limit)
    else:
        raise ValidationError("LIMIT_MUST_BE_AN_INTEGER")

    return result

def validate_products_offset(offset):
    result = None
    
    if offset.isnumeric():
        if int(offset) < 0:
            raise ValidationError("OFFSET_CANNOT_BE_A_NEGATIVE_NUMBER")# 음수 금지
        result = int(offset)
    else:
        raise ValidationError("OFFSET_MUST_BE_AN_INTEGER")

    return result

def validate_products_start_end_date(start_date, end_date):
    try:
        if start_date and end_date:
            strp_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            strp_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

            if strp_start_date > strp_end_date:
                raise ValidationError("START_DATE_MUST_BE_LESS_THAN_END_DATE")
        elif start_date or end_date:
            raise ValidationError("BOTH_NONE_OR_BOTH_DATES")

    except ValueError:
        raise ValidationError("DATE_FORMAT_MUST_BE_'YYYY-MM-DD'")

def validate_products_product_id(product_id):
    result = None

    if product_id:
        if product_id.isnumeric():
            if int(product_id) < 1:
                raise ValidationError("PRODUCT_ID_MUST_BE_GREATER_THAN_1")
            result = int(product_id)
        else:
            raise ValidationError("PRODUCT_ID_MUST_BE_A_NUMBER")

    return result

def validate_products_is_sold(is_sold):
    result = None

    if is_sold:
        if is_sold.isnumeric():
            is_sold = int(is_sold)
            if is_sold != 0 and is_sold != 1:
                raise ValidationError("IS_SOLD_MUST_BE_IN_[0, 1, None]")
        else:
            raise ValidationError("IS_SOLD_CANNOT_BE_A_STRING")
    return result

def validate_products_is_displayed(is_displayed):
    result = None

    if is_displayed:
        if is_displayed.isnumeric():
            is_displayed = int(is_displayed)
            if is_displayed != 0 and is_displayed != 1:
                raise ValidationError("IS_DISPLAYED_MUST_BE_IN_[0, 1, None]")
        else:
            raise ValidationError("IS_DISPLAYED_CANNOT_BE_A_STRING")
    return result

def validate_products_is_discounted(is_discounted):
    result = None

    if is_discounted:
        if is_discounted.isnumeric():
            is_discounted = int(is_discounted)
            if is_discounted != 0 and is_discounted != 1:
                raise ValidationError("IS_DISCOUNTED_MUST_BE_IN_[0, 1, None]")
        else:
            raise ValidationError("IS_DISCOUNTED_CANNOT_BE_A_STRING")
    return result

def validate_products_seller_property_ids(seller_property_ids):
    if seller_property_ids:
        for seller_property_id in seller_property_ids:
            if not isinstance(seller_property_id, int):
                raise ValidationError("SELLER_PROPERTY_ID_MUST_BE_AN_INTERGER")

def validate_product_code(code):
    uuid_regex = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    if not re.match(uuid_regex, code):
        raise ValidationError("INVALID_PRODUCT_CODE")

#수정기능추가
class Validation_managers_name(AbstractRule):
    
    def validate(self, value):
        errors = []
        managers_name_reg = re.compile(r"[ᄀ-힣]")
        regex       = re.compile(managers_name_reg)

        if not regex.match(value):
            errors.append('한글만 입력해주세요.')
        return errors

class Validation_managers_email(AbstractRule):
    
    def validate(self, value):
        errors = []
        managers_email_reg = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        regex        = re.compile(managers_email_reg)

        if not regex.match(value):
            errors.append('이메일 형식에 맞게 입력해주세요')
        return errors

class Validation_bank_name(AbstractRule):
    
    def validate(self, value):
        errors = []
        bank_name_reg = [
            '한국은행', 
            '산업은행',
            '기업은행',
            '국민은행',
            '수협중앙회',
            '수출입은행',
            '농협중앙회',
            '지역 농축협',
            '우리은행',
            'SC은행',
            '한국씨티은행',
            '대구은행',
            '부산은행',
            '광주은행',
            '제주은행',
            '전북은행',
            '경남은행',
            '새마을금고중앙회',
            '신협중앙회',
            '상호저축은행',
            '모건스탠리은행',
            'HSC은행',
            '도이치은행',
            '알비에스피엘씨은행',
            '제이피모간체이스은행',
            '미즈호은행',
            '미쓰비시도쿄UFJ은행',
            'BOA은행',
            '산림조합중앙회',
            '우체국',
            '신용보증기금',
            '기술보증기금',
            'KEB하나은행',
            '신한은행',
            '케이뱅크',
            '카카오뱅크',
            '한국주택금융공사',
            '한국주택금융공사',
            '서울보증보험',
            '경찰청',
            '한국전자금융(주)',
            '금융결제원'
            ]

        if value not in bank_name_reg:
            errors.append('해당되지 않는 은행 이름입니다.')
        return errors

class Validation_account_number(AbstractRule):

    def validate(self, value):
        errors = []
        account_number_reg = r"[0-9]"
        regex              = re.compile(account_number_reg)

        if not regex.match(value):
            errors.append('입력하신 계좌번호가 유효하지 않습니다.')
        return errors

class Validation_account_name(AbstractRule):

   def validate(self, value):
        errors = []
        account_name_reg = re.compile(r"[ᄀ-힣]")
        regex            = re.compile(account_name_reg)
        
        if not regex.match(value):
            errors.append('한글만 입력해주세요.')
        return errors

class Validation_shipping_information(AbstractRule):

    def validate(self, value):
        errors = []
        shipping_information_reg = re.compile(r"[ᄀ-힣a-zA-Z0-9]")
        regex                    = re.compile(shipping_information_reg)

        if not regex.match(value):
            errors.append('한글, 숫자, 영문만 입력해주세요.')
        return errors

class Validation_exchange_refund_information(AbstractRule):

    def validate(self, value):
        errors = []
        exchange_refund_information_reg = re.compile(r"[ᄀ-힣a-zA-Z0-9]")
        regex                    = re.compile(exchange_refund_information_reg)

        if not regex.match(value):
            errors.append('한글, 숫자, 영문만 입력해주세요.')
        return errors

class Validation_model_height(AbstractRule):

    def validate(self, value):
        errors = []
        model_height_reg = re.compile(r'\d{3}')
        regex            = re.compile(model_height_reg)

        if not regex.match(value):
            errors.append('숫자만 입력해주세요.')
        return errors

class Validation_model_top_size(AbstractRule):
    
    def validate(self, value):
        errors = []
        model_top_size_reg = re.compile(r'\d{2}')
        regex              = re.compile(model_top_size_reg)

        if not regex.match(value):
            errors.append('숫지만 입력해주세요.')
        return errors

class Validation_model_bottom_size(AbstractRule):
    
    def validate(self, value):
        errors = []
        model_bottom_size_reg = re.compile(r'\d{2}')
        regex              = re.compile(model_bottom_size_reg)

        if not regex.match(value):
            errors.append('숫지만 입력해주세요.')
        return errors

class Validation_model_feet_size(AbstractRule):
    
    def validate(self, value):
        errors = []
        model_feet_size_reg = re.compile(r'\d{3}')
        regex              = re.compile(model_feet_size_reg)

        if not regex.match(value):
            errors.append('숫지만 입력해주세요.')
        return errors

class Validation_shopping_feedtext(AbstractRule):
    
    def validate(self, value):
        errors = []
        shopping_feedtext_reg = re.compile(r"[ᄀ-힣a-zA-Z0-9]")
        regex   = re.compile(shopping_feedtext_reg)

        if not regex.match(value):
            errors.append('힌글, 영문, 숫자만 입력해주세요.')
        return errors