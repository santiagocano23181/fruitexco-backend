import json
from flask import Blueprint, jsonify, request, session
from sqlalchemy import and_
from models.Sale.Sale import Sales
from models.Sale.SaleStatus import SaleStatus
from models.Sale.SaleDetail import SaleDetail
from models.Sale.Discount import Discount
from models.Sale.DiscountDetail import DiscountDetail
from models.Product.Products import Products
from marshmallow_sqlalchemy.fields import Nested
from utils.db import db
from utils.ma import ma

sale = Blueprint('sale', __name__)

class SaleStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleStatus
        include_fk = True

class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        include_fk = True
        load_instance = True
    status = Nested(SaleStatusSchema)

class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True
        load_instance = True
    status = Nested(SaleSchema)

sale_schema = SaleSchema()
many_sale_schema = SaleSchema(many=True)

@sale.route('/')
def create_sale():
    try:
        id = session.get('Authorization')
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(and_(Sales.status_id==sale_status.id, Sales.client_id==id)).order_by(Sales.created_on).first()
        if(sales == None):
            sales = Sales(id, sale_status.id, 0)
            db.session.add(sales)
            db.session.commit()
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500

@sale.route('/actual')
def get_actual():
    try:
        id = session.get('Authorization')
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(and_(Sales.status_id==sale_status.id, Sales.client_id==id)).order_by(Sales.created_on).first()
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route('/calculate')
def calculate_actual():
    try:
        addition = 0
        id = session.get('Authorization')
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(and_(Sales.status_id==sale_status.id, Sales.client_id==id)).order_by(Sales.created_on).first()
        sale_details = SaleDetail.query.filter(sale_id=sales.id).all()
        discount = Discount.query.filter_by(finish_date=None).first()
            
        for sale_detail in sale_details:
            neto = 0
            product = Products.query.get(sale_detail.products_id)
            neto = product.price * sale_detail.cantity
            discount_detail = DiscountDetail(discount.id, sale_detail.id)
            if discount_detail != None:
                neto = neto - (neto * (discount.amount / 100))
            addition = addition + neto
        sales.total = addition
        db.session.commit()
        return sale_schema.jsonify(addition=addition)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500

@sale.route('/count')
def count_actual():
    try:
        id = session.get('Authorization')
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(and_(Sales.status_id==sale_status.id, Sales.client_id==id)).order_by(Sales.created_on).first()
        if sales == None:
            return jsonify(0)
        sale_count = SaleDetail.query.filter(sale_id=sales.id).count()

        return jsonify(cantity=sale_count)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500