import json
from flask import Blueprint, jsonify, request
from models.User.UserStatus import UserStatus
from utils.db import db
from utils.ma import ma

user_status = Blueprint('user_status', __name__)

class StatusUserSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusUserSchema()
many_status_schema = StatusUserSchema(many=True)

@user_status.route('/')
def list_user_status():
    try:
        status = UserStatus.query.all()
        return many_status_schema.jsonify(status)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@user_status.route('/new', methods=['PUT'])
def create_user_status():
    try:
        new_user_status = UserStatus(request.json['name'])
        db.session.add(new_user_status)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@user_status.route('/delete/<id>', methods=['DELETE'])
def delete_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(user_status)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@user_status.route('/update/<id>', methods=['PUT'])
def update_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        user_status.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@user_status.route('/get/<id>')
def get_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return status_schema.jsonify(user_status)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500