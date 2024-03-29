from flask import Blueprint, jsonify, request
from models.Sale.Domicile import Domicile
from models.Sale.DomicileDetail import DomicileDetail
from models.Sale.Sale import Sales
from models.Sale.SaleStatus import SaleStatus
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
        return jsonify(messages=str(ex), context=3), 500

@domicile.route('/', methods=['POST'])
def create_domicile():
    try:
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        actual = datetime.now()
        domicile = Domicile.query.filter_by(
            finish_date=None).first()
        domicile.finish_date = actual
        new_domicile_status = Domicile(request.json['price'])
        db.session.add(new_domicile_status)
        db.session.commit()
        
        query = db.session.query(DomicileDetail).filter(
            DomicileDetail.sale_id == Sales.id,
            Sales.status_id == sale_status.id
        )
        query.update({DomicileDetail.domicile_id: new_domicile_status.id},synchronize_session=False)
        db.session.commit()
        return jsonify(messages='Domicilio actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    