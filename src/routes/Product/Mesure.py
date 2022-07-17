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
        return jsonify({"message": str(ex)}), 500
    
@mesure.route('/new', methods=['PUT'])
def create_mesure():
    try:
        new_mesure = Mesure(request.json['name'])
        db.session.add(new_mesure)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@mesure.route('/delete/<id>', methods=['DELETE'])
def delete_mesure(id):
    try:
        mesure=Mesure.query.get(id)
        if mesure == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(mesure)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@mesure.route('/update/<id>', methods=['PUT'])
def update_mesure(id):
    try:
        mesure=Mesure.query.get(id)
        if mesure == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        mesure.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@mesure.route('/get/<id>')
def get_mesure(id):
    try:
        user_status=Mesure.query.get(id)
        if user_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return mesure_schema.jsonify(user_status)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500