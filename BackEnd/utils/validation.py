import re

from .custom_error import CustomException
# CustomException 만든이유: flask에서 지원해주는 wtforms라는 모듈의 validationError를 사용,module인식이 안되는 문제
# 커스텀클래스를 만들어서 에러메세지만 띄어주게끔 만듦

def validation_seller_account(seller_account):
    seller_account_reg = r"^[0-9a-zA-Z][0-9a-zA-Z_-]{5,20}$"
    regex  = re.compile(seller_account_reg)
    #정규 표현식을 파이썬 형식으로 읽을 수 있도록 컴파일한다. 
    if not regex.match(seller_account):
        raise CustomException('아이디는 5~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다.')

def validation_password(password):
    password_reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$"
    regex        = re.compile(password_reg)
    
    if not regex.match(password):
        raise CustomException('8~20글자의  영문대소문자, 숫자, 특수문자 조합을 사용해주세요.')

def validation_phone_number(phone_number):
    phone_number_reg = re.compile(r'\d{3}-\d{3,4}-\d{4}')
    regex        = re.compile(phone_number_reg)

    if not regex.match(phone_number):
        raise CustomException('올바른 전화번호 형식으로 작성해주세요.')

def validation_korean_name(korean_name):
    korean_name_reg = re.compile(r"[ᄀ-힣a-zA-Z0-9]")
    regex       = re.compile(korean_name_reg)
    
    if not regex.match(korean_name):
        raise CustomException('한글,영문,숫자만 입력해주세요.')

def validation_english_name(english_name):
    english_name_reg = re.compile(r"[a-z]")
    regex  = re.compile(english_name_reg)

    if not regex.match(english_name):
        raise CustomException('셀러 영문명은 소문자만 입력가능합니다.')

def validation_cs_phone(cs_phone):
    cs_phone_reg = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')
    regex    = re.compile(cs_phone_reg)

    if not regex.match(cs_phone):
        raise CustomException('고객센터 전화번호는 숫자와 하이픈만 입력가능합니다.')

#정해져 있는 특정한 키워드명인지 확인한다.
def validation_search_keyword(search_keyword):
    search_keywords = ['id','seller_account','english_name','korean_name','manager_name','seller_status','manager_phone','manager_email','seller_property','registered_product_count','register_date']

    if search_keyword not in search_keywords:
        raise CustomException('잘못된 키워드입니다.')