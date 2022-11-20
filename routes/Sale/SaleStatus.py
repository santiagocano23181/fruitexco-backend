import json
from flask import Blueprint, jsonify, request
from models.Sale.SaleStatus import SaleStatus
from utils.db import db
from utils.ma import ma

sale_status = Blueprint('sale_status', __name__)

class StatusSaleSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusSaleSchema()
many_status_schema = StatusSaleSchema(many=True)

@sale_status.route('/')
def list_sale_status():
    try:
        status = SaleStatus.query.all()
        return many_status_schema.jsonify(status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@sale_status.route('/', methods=['POST'])
def create_sale_status():
    try:
        new_sale_status = SaleStatus(request.json['name'])
        db.session.add(new_sale_status)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@sale_status.route('/<id>', methods=['DELETE'])
def delete_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(sale_status)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@sale_status.route('/<id>', methods=['PUT'])
def update_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        sale_status.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@sale_status.route('/<id>')
def get_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return status_schema.jsonify(sale_status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500