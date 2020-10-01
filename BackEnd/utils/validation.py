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
                2020 - -0 - 29(wldus9503@gmail.com) : 클래스 Validation_order 추가, DB ORDER기능 위한것
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
        order = [
            'asc', 
            'desc',
            'ASC',
            'DESC'
            ]
            
        if value not in order:
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