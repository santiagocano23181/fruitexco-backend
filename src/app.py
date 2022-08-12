from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from decouple import config
from routes.User import UserStatus, Role, User
from routes.Product import Products, Mesure, ProductStatus, Taste
from routes.Sale import SaleStatus

app = Flask(__name__)

#Configurations
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

def page_not_found(error):
    return '<h1>Page not found<h1>', 404

# Product Blueprints
app.register_blueprint(Products.products, url_prefix='/api/v1/product')
app.register_blueprint(ProductStatus.product_status, url_prefix='/api/v1/product_status')
app.register_blueprint(Mesure.mesure, url_prefix='/api/v1/mesure')
app.register_blueprint(Taste.taste, url_prefix='/api/v1/taste')

# User Blueprints
app.register_blueprint(UserStatus.user_status, url_prefix='/api/v1/user_status')
app.register_blueprint(Role.role, url_prefix='/api/v1/role')
app.register_blueprint(User.users, url_prefix='/api/v1/user')

# Sale Blueprints
app.register_blueprint(SaleStatus.sale_status, url_prefix='/api/v1/sale_status')

# Error handlers
app.register_error_handler(404, page_not_found)

