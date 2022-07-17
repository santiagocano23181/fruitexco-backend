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
        return jsonify({"message": str(ex)}), 500
    
@role.route('/new', methods=['PUT'])
def create_role():
    try:
        new_role = Role(request.json['name'])
        print(new_role)
        db.session.add(new_role)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@role.route('/delete/<id>', methods=['DELETE'])
def delete_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@role.route('/update/<id>', methods=['PUT'])
def update_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        role.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@role.route('/get/<id>')
def get_role(id):
    try:
        role=Role.query.get(id)
        if role == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return role_schema.jsonify(role)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500