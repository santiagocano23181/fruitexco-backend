import json
from flask import Blueprint, jsonify, request, session
from sqlalchemy import and_
from models.Sale.Sale import Sales
from models.Sale.SaleStatus import SaleStatus
from models.Sale.SaleDetail import SaleDetail
from marshmallow_sqlalchemy.fields import Nested
from utils.db import db
from utils.ma import ma

sale = Blueprint('sale', __name__)


class SaleStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleStatus
        include_fk = True

class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True

class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        include_fk = True
        load_instance = True
    status = Nested(SaleStatusSchema)
    detail = Nested(SaleDetailSchema)

sale_schema = SaleSchema()
many_sale_schema = SaleSchema(many=True)

@sale.route('/', methods=['POST'])
def create_sale():
    try:
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(status_id=sale_status.id).order_by(Sales.created_on)
        if(sales == None):
            id = session.get('Authorization')
            sales = Sales(id, sale_status.id, 0)
            db.session.add(sales)
            db.session.commit()
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@sale.route('/actual')
def get_actual():
    try:
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sales = Sales.query.filter(status_id=sale_status.id).order_by(Sales.created_on)
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500