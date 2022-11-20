from flask import Blueprint, jsonify, request
from models.Sale.Discount import Discount
from datetime import datetime
from utils.db import db
from utils.ma import ma

discount = Blueprint('discount', __name__)

class DiscountSchema(ma.Schema):
    class Meta:
        fields = ('id','amount', 'needed')
        
discount_schema = DiscountSchema()
many_discount_schema = DiscountSchema(many=True)
    
@discount.route('/')
def get_last_discount():
    try:
        discount = Discount.query.filter_by(
            finish_date=None).first()
        if discount == None:
            discount = Discount(0, 0)
            db.session.add(discount)
            db.session.commit()
        return discount_schema.jsonify(discount), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500

@discount.route('/', methods=['POST'])
def create_discount():
    try:
        actual = datetime.now()
        discount = Discount.query.filter_by(
            finish_date=None).first()
        discount.finish_date = actual
        new_discount_status = Discount(request.json['amount'], request.json['needed'])
        db.session.add(new_discount_status)
        db.session.commit()
        return jsonify(messages='Descuento general actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    