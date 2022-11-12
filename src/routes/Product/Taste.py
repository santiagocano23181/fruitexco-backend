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
        return jsonify(messages=str(ex), context=3), 500
    
@taste.route('/', methods=['POST'])
def create_taste():
    try:
        new_taste = Taste(request.json['name'])
        db.session.add(new_taste)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@taste.route('/<id>', methods=['DELETE'])
def delete_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(taste)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@taste.route('/<id>', methods=['PUT'])
def update_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        taste.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@taste.route('/<id>')
def get_taste(id):
    try:
        taste=Taste.query.get(id)
        if taste == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return taste_schema.jsonify(taste)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500