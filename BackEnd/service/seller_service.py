class SellerService:
    def __init__(self, dao, config):
        self.dao = dao
        self.config = config

    def search_sellers(self, search_term, limit):
        return self.dao.find_sellers_by_search_term(search_term, limit)