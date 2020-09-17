from flask import Flask
from flask_cors import CORS

from sqlalchemy import create_engine

from model import ProductDao
from service import ProductService
from view import create_endpoints

class Services:
    pass

def create_app(test_config = None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)

    product_dao = ProductDao(database)

    services = Services
    services.product_service = ProductService(product_dao, app.config)

    create_endpoints(app, services)

    return app
