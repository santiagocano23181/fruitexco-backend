from flask import Blueprint, jsonify, request
from models.Sale.Domicile import Domicile
from datetime import datetime
from utils.db import db
from utils.ma import ma

domicile = Blueprint('domicile', __name__)

class DomicileSchema(ma.Schema):
    class Meta:
        fields = ('id','price')
        
domicile_schema = DomicileSchema()
many_domicile_schema = DomicileSchema(many=True)
    
@domicile.route('/')
def get_last_domicile():
    try:
        domicile = Domicile.query.filter_by(
            finish_date=None).first()
        if domicile == None:
            domicile = Domicile(0)
            db.session.add(domicile)
            db.session.commit()
        return domicile_schema.jsonify(domicile), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@domicile.route('/new', methods=['PUT'])
def create_domicile():
    try:
        actual = datetime.now()
        domicile = Domicile.query.filter_by(
            finish_date=None).first()
        domicile.finish_date = actual
        new_domicile_status = Domicile(request.json['price'])
        db.session.add(new_domicile_status)
        db.session.commit()
        return jsonify({'message': 'Domicilio actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    