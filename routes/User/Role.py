import json
from flask import Blueprint, jsonify, request
from models.User.Role import Role
from utils.db import db
from utils.ma import ma

role = Blueprint('role', __name__)

class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
role_schema = RoleSchema()
many_role_schema = RoleSchema(many=True)

@role.route('/')
def list_role():
    try:
        roles = Role.query.all()
        return many_role_schema.jsonify(roles)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@role.route('/', methods=['POST'])
def create_role():
    try:
        new_role = Role(request.json['name'])
        db.session.add(new_role)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=2), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@role.route('/<id>', methods=['DELETE'])
def delete_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        db.session.delete(role)
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@role.route('/<id>', methods=['PUT'])
def update_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        role.name = request.json['name']
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@role.route('/<id>')
def get_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        return role_schema.jsonify(role)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500