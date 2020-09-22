import pymysql

from flask      import Flask
from flask_cors import CORS

from model   import ProductDao, SellerDao
from service import ProductService, SellerService
from view    import create_endpoints

import config

class Services:
    pass

# 작성자: 김태수
# 수정일: 2020.09.21.월
def create_app(test_config = None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    db = config.database

    product_dao = ProductDao(db)
    seller_dao = SellerDao(db)

    services = Services

    services.product_service = ProductService(product_dao, app.config)
    services.seller_service  = SellerService(seller_dao, app.config)

    create_endpoints(app, services)

    return app
