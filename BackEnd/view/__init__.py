from .product_view import CountryOfOriginView

def create_endpoints(app, services):
    product_service = services.product_service

    # 작성자: 김태수
    # 작성일: 2020.09.17.목
    # 원산지 데이터 endpoint
    app.add_url_rule('/country_of_origin/<int:country_id>', view_func = CountryOfOriginView.as_view('country_of_origin', product_service))
