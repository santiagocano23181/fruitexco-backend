import json
from flask import Blueprint, jsonify, request, session
from sqlalchemy import and_
from models.Product.Products import Products
from models.Sale.Discount import Discount
from models.Sale.DiscountDetail import DiscountDetail
from models.Sale.Domicile import Domicile
from models.Sale.SaleDetail import SaleDetail
from models.Sale.SaleStatus import SaleStatus
from models.Sale.Sale import Sales
from marshmallow_sqlalchemy.fields import Nested
from utils.db import db
from utils.ma import ma

sale_detail = Blueprint('sale_detail', __name__)


class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True


sale_detail_schema = SaleDetailSchema()
many_sale_detail_schema = SaleDetailSchema(many=True)


@sale_detail.route('/', methods=['POST'])
def create_sale():
    try:
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sale = Sales.query.filter(
            status_id=sale_status.id).order_by(Sales.created_on).first()
        sale_details = SaleDetail(
            sale.id, request.json['product_id'], request.json['cantity'])
        product = Products.query.get(request.json['product_id'])
        discount = Discount.query.filter_by(finish_date=None).first()
        db.session.add(sale_details)

        if(discount.needed <= request.json['cantity']):
            discount_detail = DiscountDetail(discount.id, sale_details.id)
            db.session.add(discount_detail)

        db.session.commit()
        return sale_detail_schema.jsonify(sale_detail)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@sale_detail.route('/cantitiy/<id>', methods=['PATCH'])
def create_sale(id):
    try:
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sale = Sales.query.filter(
            status_id=sale_status.id).order_by(Sales.created_on).first()
        sale_details = SaleDetail.query.filter(and_(
            sale_id=sale.id, products_id=id)).first()
        sale_details.cantity = request.json['cantity']

        discount = Discount.query.filter_by(finish_date=None).first()
        db.session.add(sale_details)

        if(discount.needed <= request.json['cantity']):
            discount_detail = DiscountDetail(discount.id, sale_details.id)
            db.session.add(discount_detail)
        else:
            discount_detail = DiscountDetail.query.filter(
                and_(discount.id, sale_details.id)).first()
            if(discount_detail != None):
                db.session.delete(discount_detail)
        db.session.commit()
        return sale_detail_schema.jsonify(sale_detail)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@sale_detail.route('/<id>', methods=['DELETE'])
def create_sale(id):
    try:
        sale_status = SaleStatus.query.filter_by(name='EN CARRITO').first()
        sale = Sales.query.filter(
            status_id=sale_status.id).order_by(Sales.created_on).first()
        sale_details = SaleDetail.query.filter(and_(
            sale_id=sale.id, products_id=id)).first()

        discount = Discount.query.filter_by(finish_date=None).first()

        discount_detail = DiscountDetail.query.filter(
            and_(discount.id, sale_details.id)).first()
        if(discount_detail != None):
            db.session.delete(discount_detail)
        db.session.delete(sale_details)
        db.session.commit()
        return sale_detail_schema.jsonify(sale_detail)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
