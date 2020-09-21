# 작성자: 김태수
# 작성일: 2020.09.17.목
# Product에 관련된 로직을 처리하는 class
class ProductService:
    def __init__(self, product_dao, config):
        self.product_dao = product_dao
        self.config = config

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

