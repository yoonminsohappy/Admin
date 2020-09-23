import boto3

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
    def get_country_of_origin(self, country_id):
        try:
            country_data = self.product_dao.get_country_of_origin(country_id)
        except:
            raise
        else:
            return country_data

    def find_first_categories_by_seller_property_id(self, seller_property_id):
        return self.product_dao.find_first_categories_by_seller_property_id(seller_property_id)

    def find_second_categories_by_first_category_id(self, first_category_id):
        return self.product_dao.find_second_categories_by_first_category_id(first_category_id)

    def upload_image_to_s3(self, image, filename):
        self.s3.upload_fileobj(
            image,
            self.config['S3_BUCKET'],
            filename
        )

        image_url = f"{self.config['S3_BUCKET_URL']}{filename}"
        print(image_url)
        return