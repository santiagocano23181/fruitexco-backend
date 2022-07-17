import json
from flask import Blueprint, jsonify, request
from models.Product.Taste import Taste
from utils.db import db
from utils.ma import ma

taste = Blueprint('taste', __name__)

class TasteSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
taste_schema = TasteSchema()
many_taste_schema = TasteSchema(many=True)

@taste.route('/')
def list_taste():
    try:
        tastes = Taste.query.all()
        return many_taste_schema.jsonify(tastes)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@taste.route('/new', methods=['PUT'])
def create_taste():
    try:
        new_taste = Taste(request.json['name'])
        print(new_taste)
        db.session.add(new_taste)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@taste.route('/delete/<id>', methods=['DELETE'])
def delete_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(taste)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@taste.route('/update/<id>', methods=['PUT'])
def update_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        taste.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@taste.route('/get/<id>')
def get_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return taste_schema.jsonify(taste)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500