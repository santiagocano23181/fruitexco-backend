from itertools import product
import json
from flask import Blueprint, jsonify, request
from models.Product.Products import Products
from models.Product.Mesure import Mesure
from models.Product.Taste import Taste
from models.Product.ProductStatus import ProductStatus
from utils.db import db
from utils.ma import ma

products = Blueprint('products', __name__)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        include_fk = True
        
product_schema = ProductSchema()
many_product_schema = ProductSchema(many=True)

class MesureSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
mesure_schema = MesureSchema()
many_status_schema = MesureSchema(many=True)

class TasteSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
taste_schema = TasteSchema()
many_taste_schema = TasteSchema(many=True)

class StatusProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusProductSchema()
many_status_schema = StatusProductSchema(many=True)

@products.route('/')
def list_products():
    try:
        product = Products.query.all()
        products = json.loads(many_product_schema.dumps(product))
        for p in products:
            p['mesure'] = get_mesure(p['mesure_id'])
            p['taste'] = get_taste(p['taste_id'])
            p['status'] = get_status(p['status_id'])
        return jsonify(products)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@products.route('/get/<int:id>')
def get_product(id):
    try:
        product = Products.query.get(id)
        p = json.loads(status_schema.dumps(product))
        p['mesure'] = get_mesure(p['mesure_id'])
        p['taste'] = get_taste(p['taste_id'])
        p['status'] = get_status(p['status_id'])
        return jsonify(products)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@products.route('/new', methods=['PUT'])
def create_products():
    try:
        new_product = Products(request.json['price'],
                               request.json['photo'],
                               request.json['mesure_id'],
                               request.json['taste_id'],
                               request.json['status_id'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@products.route('/delete/<id>', methods=['DELETE'])
def delete_products(id):
    try:
        product=Products.query.get(id)
        if product == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@products.route('/update/<id>', methods=['PUT'])
def update_product(id):
    try:
        product=Products.query.get(id)
        if product == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        product.price = request.json['price']
        product.photo = request.json['photo']
        product.mesure_id = request.json['mesure_id']
        product.taste_id = request.json['taste_id']
        product.status_id = request.json['status_id']
        
        db.session.commit()
        
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
def get_mesure(id: int):
    mesure = Mesure.query.get(id)
    return json.loads(mesure_schema.dumps(mesure))

def get_taste(id: int):
    taste = Taste.query.get(id)
    return json.loads(taste_schema.dumps(taste))

def get_status(id: int):
    status = ProductStatus.query.get(id)
    return json.loads(status_schema.dumps(status))
    