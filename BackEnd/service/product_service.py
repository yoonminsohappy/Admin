import boto3
import uuid

from werkzeug.utils import secure_filename

from exceptions import NonPrimaryImageError, NonImageFilenameError

# 작성자: 김태수
# 작성일: 2020.09.17.목
# Product에 관련된 로직을 처리하는 class
class ProductService:
    def __init__(self, product_dao, config):
        self.product_dao = product_dao
        self.config      = config
        self.s3          = boto3.client(
            "s3",
            aws_access_key_id     = config['S3_ACCESS_KEY'],
            aws_secret_access_key = config['S3_SECRET_KEY']
        )

    # 작성자: 김태수
    # 작성일: 2020.09.17.목
    # 원산지 데이터를 처리하는 로직
    def get_country_of_origin(self, db, country_id):
        try:
            country_data = self.product_dao.get_country_of_origin(db, country_id)
        except:
            raise
        else:
            return country_data

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

        # 상품 코드는 유니크 해야하기 때문에 uuid 식별자 사용
        code = str(uuid.uuid4())
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
        params['is_displayed']   = is_displayed
        params['is_discounted'] = is_discounted
        return self.product_dao.find_products(conn, params)

    def get_product_by_code(self, conn, code):
        product_dict = self.product_dao.find_product_by_code(conn, code)
        images_dict  = self.product_dao.find_product_images(conn, product_dict['product_id'])
        options_dict = self.product_dao.find_product_options(conn, product_dict['product_id'])

        product_dict["images"]  = images_dict
        product_dict["options"] = options_dict
        return product_dict

    def get_countries(self, conn):
        return self.product_dao.find_all_countries(conn)

    def get_colors(self, conn):
        return self.product_dao.find_all_colors(conn)

    def get_sizes(self, conn):
        return self.product_dao.find_all_sizes(conn)