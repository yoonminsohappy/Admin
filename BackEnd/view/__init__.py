from .product_view import CountryOfOriginView
from .seller_view  import SellerView

def create_endpoints(app, services):
    product_service = services.product_service
    seller_service  = services.seller_service

    # 작성자: 김태수
    # 작성일: 2020.09.17.목
    # 원산지 데이터 endpoint
    app.add_url_rule('/country_of_origin/<int:country_id>', view_func = CountryOfOriginView.as_view('country_of_origin', product_service))

    # sellers
    app.add_url_rule('/sellers', view_func = SellerView.as_view('find_sellers_by_search_term', seller_service))
