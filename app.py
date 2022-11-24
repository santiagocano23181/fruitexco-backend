from email.mime import message
from flask import Flask
from config import config as con
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from decouple import config as env
from routes.User import UserStatus, Role, User
from routes.Product import Products, Mesure, ProductStatus, Taste, Section
from routes.Sale import SaleStatus, Discount, Domicile, Sale, SaleDetail
from flask import request, jsonify, session
from utils.db import db
import jwt

app = Flask(__name__)

# Configurations
if env('PRODUCTION', default=False):
    app.config.from_object(con['production'])
else:
    app.config.from_object(con['development'])


ma = Marshmallow(app)
cors = CORS(app, resources={
            r'/api/*': {'origins': '*', 'supports_credentials': True}})


def page_not_found(error):
    return '<h1>Page not found<h1>', 404

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# Product Blueprints
app.register_blueprint(Products.products, url_prefix='/api/v1/product')
app.register_blueprint(ProductStatus.product_status,
                       url_prefix='/api/v1/product_status')
app.register_blueprint(Mesure.mesure, url_prefix='/api/v1/mesure')
app.register_blueprint(Taste.taste, url_prefix='/api/v1/taste')
app.register_blueprint(Section.section, url_prefix='/api/v1/section')

# User Blueprints
app.register_blueprint(UserStatus.user_status,
                       url_prefix='/api/v1/user_status')
app.register_blueprint(Role.role, url_prefix='/api/v1/role')
app.register_blueprint(User.users, url_prefix='/api/v1/user')

# Sale Blueprints
app.register_blueprint(SaleStatus.sale_status,
                       url_prefix='/api/v1/sale_status')
app.register_blueprint(Domicile.domicile, url_prefix='/api/v1/domicile')
app.register_blueprint(Discount.discount, url_prefix='/api/v1/discount')
app.register_blueprint(SaleDetail.sale_detail, url_prefix='/api/v1/sale_detail')
app.register_blueprint(Sale.sale, url_prefix='/api/v1/sale')

# Error handlers
app.register_error_handler(404, page_not_found)

# Middlewares


@app.before_request
def session_middleware():
    auth = request.headers.get('Authorization')
    method = request.method
    if(method != 'OPTIONS'):
        if(auth):
            value = jwt.decode(auth, env('SECRET_KEY'),
                               algorithms=['HS256'])
            session['Authorization'] = value['id']
        else:
            url = request.base_url
            if not 'user' in url:
                return jsonify(message='Usuario no valido', context=3), 403


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
    
if __name__ == '__main__':
    app.run(port=5000)