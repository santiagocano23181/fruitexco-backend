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
        return jsonify({"message": str(ex)}), 500
    
@sale_status.route('/new', methods=['PUT'])
def create_sale_status():
    try:
        new_sale_status = SaleStatus(request.json['name'])
        print(new_sale_status)
        db.session.add(new_sale_status)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@sale_status.route('/delete/<id>', methods=['DELETE'])
def delete_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(sale_status)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@sale_status.route('/update/<id>', methods=['PUT'])
def update_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        sale_status.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@sale_status.route('/get/<id>')
def get_sale_status(id):
    try:
        sale_status=SaleStatus.query.get(id)
        if sale_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return status_schema.jsonify(sale_status)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500