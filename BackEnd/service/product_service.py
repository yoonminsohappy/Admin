import boto3
import uuid
import datetime
from decimal import Decimal

from pyexcel_xls import save_data
from werkzeug.utils import secure_filename

from exceptions import NonPrimaryImageError, NonImageFilenameError, ValidationError

class ProductService:
    def __init__(self, product_dao, config):
        self.product_dao = product_dao
        self.config      = config
        self.s3          = boto3.client(
            "s3",
            aws_access_key_id     = config['S3_ACCESS_KEY'],
            aws_secret_access_key = config['S3_SECRET_KEY']
        )

    def find_first_categories_by_seller_property_id(self, conn, seller_property_id):
        """
        1차 카테고리를 셀러 속성 아이디로 조회하기 위한 서비스 레이어

        Args:
            conn              : 데이터베이스 커넥션 객체
            seller_property_id: 셀러 속성 아이디

        Returns:
            results: 1차 카테고리 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"  : 1차 카테고리 아이디,
                        "name": 1차 카테고리 이름
                    },
                    ...
                ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
        """
        return self.product_dao.find_first_categories_by_seller_property_id(conn, seller_property_id)

    def find_second_categories_by_first_category_id(self, conn, first_category_id):
        """
        2차 카테고리를 1차 카테고리 아이디로 조회하기 위한 서비스 레이어

        Args:
            conn             : 데이터베이스 커넥션 객체
            first_category_id: 1차 카테고리 아이디

        Returns:
            results: 2차 카테고리 정보를 담은 딕셔너리 리스트
                [
                    {
                        "id"  : 2차 카테고리 아이디,
                        "name": 2차 카테고리 이름
                    }
                    ...
                ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-22(이충희): 초기 생성
        """
        return self.product_dao.find_second_categories_by_first_category_id(conn, first_category_id)

    def upload_image_to_s3(self, image, filename):
        """
        S3에 이미지 업로드

        Args:
            image   : 이미지 파일
            filename: 이미지 파일 이름

        Returns:
            url: S3에 업로드된 파일 경로

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-23(이충희): 초기 생성
        """
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET'],
            filename
        )

        return f"{self.config['S3_BUCKET_URL']}{filename}"


    def search_sellers(self, conn, search_term, limit):
        """
        상품 등록에 필요한 셀러 검색을 위한 서비스 레이어

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

    def add_product(self, conn, images, body):
        """
        상품 등록을 위한 서비스 레이어
        1. JSON 및 이미지 파일 유효성 검사
        2. 상품 추가
        3. 상품 상세 추가
        4. 옵션 추가
        5. S3 이미지 업로드 및 상품 이미지 DB에 추가

        Args:
            conn  : 데이터베이스 커넥션 객체
            images: 상품 이미지 파일들
            body  : 상품 정보를 담고 있는 json 바디

        Returns:

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-27(이충희): 초기 생성
            2020-09-29(이충희): 커스텀 에러 처리 추가
        """
        product            = body['product']
        product_detail     = body['detail']
        options            = body['options']
        first_category_id  = product['first_category_id']
        second_category_id = product['second_category_id']
        # 상품 코드는 유니크 해야하기 때문에 uuid 식별자 사용
        code = str(uuid.uuid4())

        filenames = []
        for i, image in enumerate(images):
            if not image:
                if i == 0:
                    raise NonPrimaryImageError("MUST_INCLUDE_PRIMARY_IMAGE")
                continue
            
            if image.filename == '':
                raise NonImageFilenameError("MUST_INCLUDE_FILENAME")

            filename = secure_filename(image.filename)
            filename = f'{code}_{filename}'
            filenames.append(filename)

        images = [ image for image in images if image != None ]

        # 1. 상품 추가
        categories_id  = self.product_dao.find_categories_id(conn, first_category_id, second_category_id)

        product['categories_id'] = categories_id['id']
        product['code']          = code
        product_id = self.product_dao.create_product(conn, product)

        # 2. 상품 상세 추가
        product_detail['product_id'] = product_id
        self.product_dao.create_product_detail(conn, product_detail)

        # 3. 옵션 추가
        for option in options:
            option['product_id'] = product_id
            self.product_dao.create_option(conn, option)

        # 4. 이미지 S3 업로드 + 이미지 테이블 URL 추가
        for i, image in enumerate(images):
            url = self.upload_image_to_s3(image, filenames[i])
            self.product_dao.create_product_image(conn, url, i+1, product_id)

    def get_products_list(
        self, 
        conn, 
        limit, 
        offset, 
        start_date, 
        end_date, 
        seller_name,
        product_name,
        product_id,
        product_code,
        seller_property_ids,
        is_sold,
        is_displayed,
        is_discounted
    ):
        """
        상품 리스트 조회 서비스 레이어

        Args:
            conn: 데이터베이스 커넥션 객체
            limit: 몇 개의 데이터를 불러올지
            offset: 페이지네이션
            start_date: 조건 시작 날짜
            end_date: 조건 종료 날짜
            seller_name: 셀러명
            product_name: 상품 이름
            product_id: 상품 번호
            product_code: 상품 코드
            seller_property_ids: 셀러 속성 아이디 리스트
            is_sold: 판매 여부
            is_displayed: 조회 여부
            is_discounted: 할인 여부

        Returns:
            results: 
            [
                {
                    "code"         : 상품코드
                    "discount_rate": 할인율
                    "id"           : 상품 아이디
                    "image_path"   : 상품 대표 이미지 URL
                    "is_displayed" : 조회 여부
                    "is_sold"      : 판매 여부
                    "korean_name"  : 셀러 이름
                    "name"         : 상품 이름
                    "register_date": 등록 일자
                    "sale_price"   : 판매 가격
                    "sp.name"      : 셀러 속성 이름
                }
                ...
            ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-30(이충희): 초기 생성
        """
        # SQL 파라미터를 딕셔너리로 제공하기 위해 만든다.
        params = dict()
        params['limit']        = limit
        params['offset']       = offset
        params['start_date']   = start_date
        params['end_date']     = end_date
        params['seller_name']  = '%' + seller_name + '%' if seller_name else None
        params['product_name'] = '%' + product_name + '%' if product_name else None
        params['product_id']   = product_id
        params['product_code'] = product_code

        for idx, seller_property_id in enumerate(seller_property_ids):
            params[f'seller_property_id_{idx}'] = seller_property_id
        params['seller_property_ids_length'] = len(seller_property_ids)

        params['is_sold']       = is_sold
        params['is_displayed']  = is_displayed
        params['is_discounted'] = is_discounted
        return self.product_dao.find_products(conn, params)

    def get_product_by_code(self, conn, code):
        """
        상품 코드로 상품 조회하기

        Args:
            conn: 데이터베이스 커넥션 객체
            code: 상품 코드

        Returns:
            상품정보(products)
            상품상세정보(product_detail)
            상품옵션(options)
            이미지(product_images)

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-09-30(이충희): 초기 생성
        """
        # 1 to Many일 때 조인?
        product_dict = self.product_dao.find_product_by_code(conn, code)
        images_dict  = self.product_dao.find_product_images(conn, product_dict['product_id'])
        options_dict = self.product_dao.find_product_options(conn, product_dict['product_id'])

        product_dict["images"]  = images_dict
        product_dict["options"] = options_dict
        return product_dict

    def get_countries(self, conn):
        """
        제조국 리스트 조회

        Args:
            conn: 데이터베이스 커넥션 객체

        Returns:
            제조국 리스트
            [
                {
                    "id"  : 제조국 아이디
                    "name": 제조국 이름
                }
            ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희): 초기 생성
        """
        return self.product_dao.find_all_countries(conn)

    def get_colors(self, conn):
        """
        컬러 리스트 조회

        Args:
            conn: 데이터베이스 커넥션 객체

        Returns:
            컬러 리스트
            [
                {
                    "id"  : 컬러 아이디
                    "name": 컬러 이름
                }
                ...
            ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희): 초기 생성
        """
        return self.product_dao.find_all_colors(conn)

    def get_sizes(self, conn):
        """
        사이즈 리스트 조회

        Args:
            conn: 데이터베이스 커넥션 객체

        Returns:
            사이즈 리스트
            [
                {
                    "id"  : 사이즈 아이디
                    "name": 사이즈 이름
                }
                ...
            ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-02(이충희)
        """
        return self.product_dao.find_all_sizes(conn)

    def make_excel_file(self, directory, filename, results):
        """
        엑셀 파일 만들기

        Args:
            directory: 엑셀 파일 생성 경로
            filename : 엑셀 파일 생성 이름
            results  : 엑셀에 들어갈 내용

        Returns:
            directory: 엑셀 파일 생성 경로
            filename : 엑셀 파일 생성 이름

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-03(이충희)
        """
 
        data = [['등록일', '대표이미지', '상품명', '상품코드', '상품번호', '셀러속성', '셀러명', '판매가', '할인가', '판매여부', '진열여부', '할인여부']]
        for idx, item in enumerate(results):
            # 두 번째 줄 부터 데이터 넣기
            data.append([
                item['register_date'],
                item['image_path'],
                item['product_name'],
                item['code'],
                item['id'],
                item['seller_property_name'],
                item['seller_name'],
                item['sale_price'],
                int(item['discounted_price']),
                item['is_sold'],
                item['is_displayed'],
                1 if item['discount_rate'] > 0 else 0
            ])

        # now_date = datetime.datetime.now().strftime("%Y%m%d")
        # filename = now_date + "_" + filename
        save_data(directory + filename, {"data": data})
        
        return directory, filename

    def make_excel_all(self, conn, start_date, end_date):
        """
        모든 상품 엑셀 파일 만들기

        Args:
            conn      : 데이터베이스 커넥션 객체
            start_date: 조건 시작 날짜
            end_date  : 조건 종료 날짜

        Returns:
            directory: 엑셀 파일 생성 경로
            filename : 엑셀 파일 생성 이름

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-03(이충희)
        """
        results = self.product_dao.find_products_by_dates(conn, start_date, end_date)

        directory, filename =  self.make_excel_file("temp/", f"{str(uuid.uuid4())}.xls", results)
        return directory, filename, "전체상품엑셀다운로드_브랜디.xls"

    def make_excel_select(self, conn, product_ids):
        """
        선택 상품 엑셀 파일 만들기

        Args:
            conn       : 데이터베이스 커넥션 객체
            product_ids: 선택한 상품 아이디 리스트

        Returns:
            directory: 엑셀 파일 생성 경로
            filename : 엑셀 파일 생성 이름

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-03(이충희)
        """
        results = self.product_dao.find_products_by_ids(conn, product_ids)
    
        directory, filename = self.make_excel_file("temp/", f"{str(uuid.uuid4())}.xls", results)
        return directory, filename, "선택상품엑셀다운로드_브랜디.xls"

    def update_product(self, conn, product_id, images, body):
        """
        상품 이력 조회 서비스

        Args:
            conn      : 데이터베이스 커넥션 객체
            product_id: 상품 아이디
            images    : 이미지 상태와 이미지 파일 객체를 담고 있는 딕셔너리
            body      : 수정할 것이 있는 json 바디

        Returns:

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-04(이충희)
        """

        # 상품 아이디 꼭 필요. 어떤 상품을 수정할지 알아야하니까.
        product = body.get('product', None)
        if not product:
            raise ValidationError("PRODUCT_CANNOT_BE_NULL")
        product['product_id'] = int(product_id)

        # 상품 코드, 이미지 파일 이름 만들 때 필요.
        product_code = product.get('product_code', None)
        if not product_code:
            raise ValidationError("PRODUCT_CODE_CANNOT_BE_NULL")

        # 수정자 아이디를 넣어두기 위해 필요
        seller_id = product.get('seller_id', None)
        if not seller_id:
            raise ValidationError("SELLER_ID_CANNOT_BE_NULL")

        first_category_id  = product.get('first_category_id', None)
        second_category_id = product.get('second_category_id', None)

        product_detail = body.get('detail', None)
        options        = body.get('options', None)

        # 이미지 유효성 검사
        for image in images:
            if image['image_status'] == "EXIST" or \
            image['image_status'] == "DELETE" or \
            image['image_status'] == "NONE":
                continue

            # 파일이 있는가?
            if not image["image"]:
                if i == 0:
                    raise NonPrimaryImageError("MUST_INCLUDE_PRIMARY_IMAGE")
            
            # 파일명이 있는가?
            if image["image"].filename == '':
                raise NonImageFilenameError("MUST_INCLUDE_FILENAME")

            # 파일 이름 생성
            filename = secure_filename(image["image"].filename)
            filename = f'{product_code}_{filename}'
            image["filename"] = filename
            
        # 1. 상품 업데이트
        if first_category_id and second_category_id:
            result = self.product_dao.find_categories_id(conn, first_category_id, second_category_id)
            product['categories_id'] = result['id']
            self.product_dao.update_product(conn, product)

        # 2. 상품 상세 업데이트
        if product_detail:
            # 기존 상품을 딕셔너리로 가져와서
            old_product_detail = self.product_dao.find_product_detail_by_id(conn, product_id)
        
            # 수정 할 항목을 업데이트
            if product_detail.get('is_sold', None):
                old_product_detail['is_sold'] = product_detail['is_sold']

            if product_detail.get('is_displayed', None):
                old_product_detail['is_displayed'] = product_detail['is_displayed']

            if product_detail.get('origin_company', None):
                old_product_detail['origin_company'] = product_detail['origin_company']

            if product_detail.get('origin_date', None):
                old_product_detail['origin_date'] = product_detail['origin_date']

            if product_detail.get('country_of_origin_id', None):
                old_product_detail['country_of_origin_id'] = product_detail['country_of_origin_id']

            if product_detail.get('name', None):
                old_product_detail['name'] = product_detail['name']

            if product_detail.get('simple_description', None):
                old_product_detail['simple_description'] = product_detail['simple_description']

            if product_detail.get('description', None):
                old_product_detail['description'] = product_detail['description']

            if product_detail.get('sale_price', None):
                old_product_detail['sale_price'] = product_detail['sale_price']

            if product_detail.get('discount_rate', None):
                old_product_detail['discount_rate'] = product_detail['discount_rate']

            if product_detail.get('discount_started_at', None):
                old_product_detail['discount_started_at'] = product_detail['discount_started_at']

            if product_detail.get('discount_ended_at', None):
                old_product_detail['discount_ended_at'] = product_detail['discount_ended_at']
            
            if product_detail.get('minimum_sale_amount', None):
                old_product_detail['minimum_sale_amount'] = product_detail['minimum_sale_amount']
            
            if product_detail.get('maximum_sale_amount', None):
                old_product_detail['maximum_sale_amount'] = product_detail['maximum_sale_amount']

            old_product_detail['product_id'] = product_id
            old_product_detail['modifier_id'] = seller_id
            
            self.product_dao.update_product_detail(conn, old_product_detail)

        if options:
            for option in options:
                option['product_id'] = product_id
                self.product_dao.update_option(conn, option)

        # 4. 이미지 S3 업로드 + 이미지 테이블 URL 추가
        for i, image in enumerate(images):

            # NONE이면 이 뒤로는 이미지 수정하지 않음
            if image['image_status'] == "NONE":
                break
            # 이미지 수정없이 그대로
            if image['image_status'] == "EXIST":
                continue
            # 이미지 삭제
            if image['image_status'] == "DELETE":
                # 이미지가 있는지 확인
                result = self.product_dao.find_product_image(conn, product_id, i+1)
                if not result:
                    continue
                key = result['image_path'].split("/")[-1]
                # S3 이미지 삭제
                self.s3.delete_object(
                    Bucket=self.config['S3_BUCKET'],
                    Key=key
                )
                # 이미지 테이블에서 삭제
                self.product_dao.delete_product_image(conn, product_id, i+1)

            # 이미지 업로드
            if image['image_status'] == "UPLOAD":
                # 이미지 있는지 확인
                result = self.product_dao.find_product_image(conn, product_id, i+1)
                if result:
                    # 있으면 삭제 후 업로드
                    key = result['image_path'].split("/")[-1]
                    self.s3.delete_object(
                        Bucket=self.config['S3_BUCKET'],
                        Key=key
                    )
                    self.product_dao.delete_product_image(conn, product_id, i+1)
                    url = self.upload_image_to_s3(image['image'], image['filename'])
                    self.product_dao.create_product_image(conn, url, i+1, product_id)
                else:
                    # 없으면 그냥 업로드
                    url = self.upload_image_to_s3(image['image'], image['filename'])
                    self.product_dao.create_product_image(conn, url, i+1, product_id)

    def get_product_history(self, conn, product_id):
        """
        상품 이력 조회 서비스

        Args:
            conn      : 데이터베이스 커넥션 객체
            product_id: 상품 아이디

        Returns:
            상품 이력 리스트
            [
                {
                    "created_at"      : 수정이 된 날짜
                    "discount_rate"   : 할인율
                    "discounted_price": 할인가
                    "is_displayed"    : 전시여부
                    "is_sold"         : 판매여부
                    "korean_name"     : 셀러 이름
                    "sale_price"      : 원래 판매가
                },
                ...
            ]

        Author:
            이충희(choonghee.dev@gmail.com)

        History:
            2020-10-04(이충희)
        """
        results = self.product_dao.find_product_history(conn, product_id)
        for result in results:
            result['discounted_price'] = int(result['discounted_price'])
        return results