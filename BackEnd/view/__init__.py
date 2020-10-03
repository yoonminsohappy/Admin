from .product_view import (
    CountryOfOriginView,
    FirstCategoriesBySellerPropertyIdView,
    SecondCategoriesByFirstCategoryIdView,
    ProductsView,
    ProductView,
    ProductCountriesView,
    ProductColorsView,
    ProductSizesView
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
    SellerSerachView,
    SellerUpdateView
)

from .user_view import (
    UserSerachView
)

def create_endpoints(app, services):
    product_service = services.product_service
    seller_service  = services.seller_service
    order_service   = services.order_service
    user_service    = services.user_service

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
    app.add_url_rule('/sellers/signup', view_func=SellerSignUpView.as_view('seller_signup_view',seller_service))
    app.add_url_rule('/sellers/signin', view_func=SellerSignInView.as_view('seller_signin_view',seller_service))
    # 작성일: 2020.09.29.화
    app.add_url_rule('/sellers', view_func=SellerSerachView.as_view('seller_search_view',seller_service))  
    app.add_url_rule('/sellers/<int:sellers_id>', view_func=SellerUpdateView.as_view('seller_update_view',seller_service))
    # 작성일: 2020.10.01.목
    app.add_url_rule('/users',view_func=UserSerachView.as_view('user_search_view',user_service)) 