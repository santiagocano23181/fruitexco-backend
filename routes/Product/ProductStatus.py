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
        return jsonify(messages=str(ex), context=3), 500
    
@product_status.route('/', methods=['POST'])
def create_product_status():
    try:
        new_product_status = ProductStatus(request.json['name'])
        db.session.add(new_product_status)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@product_status.route('/<id>', methods=['DELETE'])
def delete_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(product_status)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@product_status.route('/<id>', methods=['PUT'])
def update_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        product_status.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@product_status.route('/<id>')
def get_product_status(id):
    try:
        product_status=ProductStatus.query.get(id)
        if product_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return status_schema.jsonify(product_status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500