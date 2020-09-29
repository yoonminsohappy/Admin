from .product_view import (
    CountryOfOriginView,
    FirstCategoriesBySellerPropertyIdView,
    SecondCategoriesByFirstCategoryIdView,
    ProductImagesUploadView,
    ProductCreationView,
)
from .order_view   import (
    GetOrderDataView,
    PutOrderStatusView,
    GetOrderDetailDataView
)
from .seller_view  import (
    ProductSellerSearchView,
    SellerSignUpView,
    SellerSignInView,
    SellerSerachView
)

def create_endpoints(app, services):
    product_service = services.product_service
    seller_service  = services.seller_service
    order_service   = services.order_service

    app.add_url_rule('/country_of_origin/<int:country_id>',
        view_func = CountryOfOriginView.as_view('country_of_origin', product_service)
    )
    app.add_url_rule('/products/sellers', 
        view_func = ProductSellerSearchView.as_view('product_seller_search_view', seller_service)

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
    app.add_url_rule('/products',
        view_func = ProductCreationView.as_view('product_creation_view', product_service)
    )
    app.add_url_rule('/order',
        view_func = GetOrderDataView.as_view('order_data_view', order_service)
    )
    app.add_url_rule('/order-status',
        view_func = PutOrderStatusView.as_view('order_status_view', order_service)
    )
    app.add_url_rule('/order-detail',
        view_func = GetOrderDetailDataView.as_view('order_detail_view', order_service)
    )
    # 작성자: 이지연
    # 작성일: 2020.09.22.화
    # 회원가입 endpoint    
    app.add_url_rule('/sellers/signup', view_func=SellerSignUpView.as_view('seller_signup_view',seller_service))
    app.add_url_rule('/sellers/signin', view_func=SellerSignInView.as_view('seller_signin_view',seller_service))
    app.add_url_rule('/sellers', view_func=SellerSerachView.as_view('seller_search_view',seller_service))
