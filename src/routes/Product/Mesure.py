import json
from flask import Blueprint, jsonify, request
from models.Product.Mesure import Mesure
from utils.db import db
from utils.ma import ma

mesure = Blueprint('mesure', __name__)

class MesureSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
mesure_schema = MesureSchema()
many_mesure_schema = MesureSchema(many=True)

@mesure.route('/')
def list_mesure():
    try:
        status = Mesure.query.all()
        return many_mesure_schema.jsonify(status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@mesure.route('/', methods=['POST'])
def create_mesure():
    try:
        new_mesure = Mesure(request.json['name'])
        db.session.add(new_mesure)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@mesure.route('/<id>', methods=['DELETE'])
def delete_mesure(id):
    try:
        mesure=Mesure.query.get(id)
        if mesure == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(mesure)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@mesure.route('/<id>', methods=['PUT'])
def update_mesure(id):
    try:
        mesure=Mesure.query.get(id)
        if mesure == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        mesure.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@mesure.route('/<id>')
def get_mesure(id):
    try:
        user_status=Mesure.query.get(id)
        if user_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return mesure_schema.jsonify(user_status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500