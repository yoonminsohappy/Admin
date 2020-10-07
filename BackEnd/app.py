import pymysql

from flask          import Flask
from flask_cors     import CORS

from model          import ProductDao, SellerDao, OrderDao, UserDao, CouponDao, EventDao
from service        import ProductService, SellerService, OrderService, UserService, CouponService, EventService
from view           import create_endpoints

class Services:
    pass

# 작성자: 김태수
# 수정일: 2020.09.21.월
def create_app(test_config = None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    product_dao = ProductDao()
    seller_dao  = SellerDao()
    order_dao   = OrderDao()
    user_dao    = UserDao()
    coupon_dao  = CouponDao()
    event_dao   = EventDao()

    services = Services

    services.product_service = ProductService(product_dao, app.config)
    services.seller_service  = SellerService(seller_dao, app.config)
    services.order_service   = OrderService(order_dao, app.config)
    services.user_service    = UserService(user_dao, app.config)
    services.coupon_service  = CouponService(coupon_dao, app.config)
    services.event_service   = EventService(event_dao, app.config)

    create_endpoints(app, services)

    return app
