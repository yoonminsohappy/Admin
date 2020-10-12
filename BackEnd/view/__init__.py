from .product_view import (
    FirstCategoriesBySellerPropertyIdView,
    SecondCategoriesByFirstCategoryIdView,
    ProductsView,
    ProductView,
    ProductCountriesView,
    ProductColorsView,
    ProductSizesView,
    ProductsDownloadView,
    ProductHistoryView
)
from .order_view   import (
    GetOrderDataView,
    PutOrderStatusView,
    GetOrderDetailDataView,
    PutAddress
)
from .seller_view  import (
    ProductSellerSearchView,
    SellerSignUpView,
    SellerSignInView,
    SellerSearchView,
    SellerUpdateView,
    SellerExcelDownloadView
)

from .user_view import (
    UserSerachView
)

from .coupon_view import (
    CouponsView,
    CouponView,
    CouponSerialsView,
    CouponCodeView
)
from .event_view import(
    EventView
)

def create_endpoints(app, services):
    product_service = services.product_service
    seller_service  = services.seller_service
    order_service   = services.order_service
    user_service    = services.user_service
    coupon_service  = services.coupon_service
    event_service   = services.event_service

    # 상품
    app.add_url_rule('/products/sellers', 
        view_func = ProductSellerSearchView.as_view('product_seller_search_view', seller_service)
    )
    app.add_url_rule('/products/first-categories',
        view_func = FirstCategoriesBySellerPropertyIdView.as_view('first_categories_by_seller_property_id_view', product_service)
    )
    app.add_url_rule('/products/second-categories',
        view_func = SecondCategoriesByFirstCategoryIdView.as_view('second_categories_by_first_category_id_view', product_service)
    )
    app.add_url_rule('/products',
        view_func = ProductsView.as_view('products_view', product_service)
    )
    app.add_url_rule('/products/<code>',
        view_func = ProductView.as_view('product_view', product_service)
    )
    app.add_url_rule('/products/countries',
        view_func = ProductCountriesView.as_view('product_countries_view', product_service)
    )
    app.add_url_rule('/products/colors',
        view_func = ProductColorsView.as_view('product_colors_view', product_service)
    )
    app.add_url_rule('/products/sizes',
        view_func = ProductSizesView.as_view('product_sizes_view', product_service)
    )
    app.add_url_rule('/products/download',
        view_func = ProductsDownloadView.as_view('products_download_view', product_service)
    )
    app.add_url_rule('/products/<int:product_id>/history',
        view_func = ProductHistoryView.as_view('product_history_view', product_service)
    )

    # 주문관리, 취소/환불 관리
    app.add_url_rule('/order',
        view_func = GetOrderDataView.as_view('order_data_view', order_service)
    )
    app.add_url_rule('/order-status',
        view_func = PutOrderStatusView.as_view('order_status_view', order_service)
    )
    app.add_url_rule('/order-detail',
        view_func = GetOrderDetailDataView.as_view('order_detail_view', order_service)
    )
    app.add_url_rule('/order-address',
        view_func = PutAddress.as_view('order_address_view', order_service)
    )
    # seller
    app.add_url_rule('/sellers/signup', view_func=SellerSignUpView.as_view('seller_signup_view',seller_service))
    app.add_url_rule('/sellers/signin', view_func=SellerSignInView.as_view('seller_signin_view',seller_service))
    app.add_url_rule('/sellers', view_func=SellerSearchView.as_view('seller_search_view',seller_service))  
    app.add_url_rule('/sellers/<int:seller_id>', view_func=SellerUpdateView.as_view('seller_update_view',seller_service))
    app.add_url_rule('/sellers/download', view_func=SellerExcelDownloadView.as_view('seller_excel_download_view', seller_service))
    app.add_url_rule('/users',view_func=UserSerachView.as_view('user_search_view',user_service)) 
    # 쿠폰
    app.add_url_rule('/coupons',view_func=CouponsView.as_view('coupons_view', coupon_service))
    app.add_url_rule('/coupons/<int:coupon_id>', view_func=CouponView.as_view('coupon_view', coupon_service))
    app.add_url_rule('/coupons/<int:coupon_id>/code', view_func=CouponCodeView.as_view('coupon_code_view', coupon_service))
    app.add_url_rule('/coupons/<int:coupon_id>/serials', view_func=CouponSerialsView.as_view('coupon_serials_view', coupon_service))

    # 기획전
    app.add_url_rule('/events', view_func=EventView.as_view('event_view', event_service))
