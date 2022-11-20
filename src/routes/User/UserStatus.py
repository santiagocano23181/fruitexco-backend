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
        return jsonify(messages=str(ex), context=3), 500
    
@user_status.route('/', methods=['POST'])
def create_user_status():
    try:
        new_user_status = UserStatus(request.json['name'])
        db.session.add(new_user_status)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@user_status.route('/<id>', methods=['DELETE'])
def delete_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(user_status)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@user_status.route('/<id>', methods=['PUT'])
def update_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        user_status.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@user_status.route('/<id>')
def get_user_status(id):
    try:
        user_status=UserStatus.query.get(id)
        if user_status == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return status_schema.jsonify(user_status)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500