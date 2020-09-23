from .product_view import (
    CountryOfOriginView,
    FirstCategoriesBySellerPropertyIdView,
    SecondCategoriesByFirstCategoryIdView,
    ProductImagesUploadView
)
from .seller_view  import SellerView

def create_endpoints(app, services):
    product_service = services.product_service
    seller_service  = services.seller_service

    # 작성자: 김태수
    # 작성일: 2020.09.17.목
    # 원산지 데이터 endpoint
    app.add_url_rule('/country_of_origin/<int:country_id>', view_func = CountryOfOriginView.as_view('country_of_origin', product_service))

    app.add_url_rule('/sellers', 
        view_func = SellerView.as_view('find_sellers_by_search_term', seller_service)
    )
    app.add_url_rule('/products/first-categories', 
        view_func = FirstCategoriesBySellerPropertyIdView.as_view('first_categories_by_seller_property_id_view', product_service)
    )
    app.add_url_rule('/products/second-categories', 
        view_func = SecondCategoriesByFirstCategoryIdView.as_view('second_categories_by_first_category_id_view', product_service)
    )
    app.add_url_rule('/products/upload-images',
        view_func = ProductImagesUploadView.as_view('product_images_upload_view', product_service)
    )
