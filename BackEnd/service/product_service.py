import boto3
import uuid

from werkzeug.utils import secure_filename

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
        return self.product_dao.find_first_categories_by_seller_property_id(conn, seller_property_id)

    def find_second_categories_by_first_category_id(self, conn, first_category_id):
        return self.product_dao.find_second_categories_by_first_category_id(conn, first_category_id)

    def upload_image_to_s3(self, image, filename):
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET'],
            filename
        )

        return f"{self.config['S3_BUCKET_URL']}{filename}"


    def search_sellers(self, conn, search_term, limit):
        return self.dao.find_sellers_by_search_term(conn, search_term, limit)

    def add_product(self, conn, images, body):
        # 1. 상품 추가
        product        = body['product']
        product_detail = body['detail']

        first_category_id  = product['first_category_id']
        second_category_id = product['second_category_id']
        categories_id  = self.product_dao.find_categories_id(conn, first_category_id, second_category_id)

        code = str(uuid.uuid4())
        product['categories_id'] = categories_id['id']
        product['code']          = code
        product_id = self.product_dao.create_product(conn, product)

        # 2. 상품 상세 추가
        product_detail['product_id'] = product_id
        self.product_dao.create_product_detail(conn, product_detail)

        # 3. 옵션 추가
        options = body['options']
        for option in options:
            option['product_id'] = product_id
            self.product_dao.create_option(conn, option)

        # 4. 이미지 S3 업로드 + 이미지 테이블 URL 추가
        filenames = []
        for i, image in enumerate(images):
            if not image:
                if i == 0:
                    raise TypeError("MUST_INCLUDE_PRIMARY_IMAGE")
                continue
            
            if image.filename == '':
                raise TypeError("MUST_INCLUDE_FILENAME")

            filename = secure_filename(image.filename)
            filename = f'{code}_{filename}'
            filenames.append(filename)

        images = [ image for image in images if image != None ]
        for i, image in enumerate(images):
            url = self.upload_image_to_s3(image, filenames[i])
            self.product_dao.create_product_image(conn, url, i+1, product_id)
