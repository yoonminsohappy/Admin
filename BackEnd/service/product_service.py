class ProductService:
    def __init__(self, product_dao, config):
        self.product_dao = product_dao
        self.config = config

    def get_country_of_origin(self, country_id):
        return self.product_dao.get_country_of_origin(country_id)
