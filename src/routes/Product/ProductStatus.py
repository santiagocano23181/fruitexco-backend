import json
from flask import Blueprint, jsonify, request
from models.Product.ProductStatus import ProductStatus
from utils.db import db
from utils.ma import ma

product_status = Blueprint('product_status', __name__)

class StatusProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusProductSchema()
many_status_schema = StatusProductSchema(many=True)

@product_status.route('/')
def list_product_status():
    try:
        status = ProductStatus.query.all()
        return many_status_schema.jsonify(status)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@product_status.route('/', methods=['POST'])
def create_product_status():
    try:
        new_product_status = ProductStatus(request.json['name'])
        print(new_product_status)
        db.session.add(new_product_status)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@product_status.route('/<id>', methods=['DELETE'])
def delete_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(product_status)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@product_status.route('/<id>', methods=['PUT'])
def update_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        product_status.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@product_status.route('/<id>')
def get_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return status_schema.jsonify(product_status)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500