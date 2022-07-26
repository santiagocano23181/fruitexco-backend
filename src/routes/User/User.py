from datetime import datetime, timedelta
from itertools import product
import json
import uuid
from flask import Blueprint, jsonify, request
from models.User.User import Users
from models.User.UserStatus import UserStatus
from models.User.Role import Role
from models.User.UserDetails import UserDetails
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db
from utils.ma import ma

users = Blueprint('users', __name__)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        exclude = ('password_user',)
        include_fk = True
        
user_schema = UserSchema()
many_user_schema = UserSchema(many=True)

class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
role_schema = RoleSchema()
many_role_schema = RoleSchema(many=True)

class UserDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDetails
        include_fk = True
        
user_details_schema = UserDetailsSchema()
many_user_details_schema = UserDetailsSchema(many=True)

class StatusUserSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusUserSchema()
many_status_schema = StatusUserSchema(many=True)

@users.route('/')
def list_users():
    try:
        user = Users.query.all()
        users = json.loads(many_user_schema.dumps(user))
        for u in users:
            u['role'] = get_role(u['role_id'])
            u['user_details'] = get_details(u['id'])
            u['status'] = get_status(u['status_id'])
        return jsonify(users)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

@users.route('/get/<int:id>')
def get_user(id):
    try:
        user = Users.query.get(id)
        u = json.loads(status_schema.dumps(user))
        u['role'] = get_role(u['role_id'])
        u['user_details'] = get_details(u['id'])
        u['status'] = get_status(u['status_id'])
        return jsonify(user)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@users.route('/new', methods=['PUT'])
def create_user():
    try:
        status = UserStatus.query.filter_by(name="INACTIVO").first()
        status_activo = UserStatus.query.filter_by(name="ACTIVO").first()
        role = Role.query.filter_by(name="USUARIO").first()
        
        if status == None:
            return jsonify({'message': 'No es posible consultar usuario porque no hay datos en la base de datos'}), 500
        
        user = Users.query.filter_by(request.json['email'], status_id=status_activo.id).first()
        
        if user != None:
            return jsonify({'message': 'El usuario ya existe en la base de datos'}), 500
        
        if user == None:
            new_user = Users(request.json['email'],
                            request.json['user_name'],
                            generate_password_hash(request.json['password_user'], method='sha256'),
                            request.json['phone'],
                            request.json['address'],
                            role.id,
                            status_activo.id)
            db.session.add(new_user)
        else:
            actual = datetime.now()
            user.email = request.json['email']
            user.user_name = request.json['user_name']
            user.guid = str(uuid.uuid4())
            user.phone = request.json['phone']
            user.password = generate_password_hash(request.json['password'], method='sha256')
            user.address = request.json['address']
            user.rol_id = request.json['rol_id']
            user.exp_time = actual + timedelta(minutes=15)
        db.session.commit()
        
        user = Users.query.filter_by(email=request.json['email']).first()
        
        new_user_details = UserDetails(user.id)
        db.session.add(new_user_details)
        db.session.commit()
        
        user = Users.query.filter_by(email=request.json['email']).first()
        
        user_dict = json.loads(user_schema.dumps(user))
        user_dict['user_datails'] = get_details(user.id)
        user_dict.pop('password')
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
    
@users.route('/login', methods=['POST'])
def create_user():
    try:
        status = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return jsonify({'message': 'No es posible consultar usuario porque no hay datos en la base de datos'}), 500
        
        user = Users.query.filter_by(email=request.json['email'], status_id=status.id).first()
        
        if not user != None or not check_password_hash(user.password, request.json['password']):
            return jsonify({'message': 'Asegurate que los datos son correctos e intentalo de nuevo'}), 404
        
        user_dict = json.loads(user_schema.dumps(user))
        user_dict['user_datails'] = get_details(user.id)
        user_dict['status'] = get_status(request.json['status_id'])
        user_dict['role'] = get_role(request.json['role_id'])
        user_dict.pop('password')
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

    
@users.route('/activate/<guid>', methods=['POST'])
def create_user(guid):
    try:
        status = UserStatus.query.filter_by(name="INACTIVO").first()
        status_activo = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return jsonify({'message': 'No es posible consultar usuario porque no hay datos en la base de datos'}), 500
        
        user = Users.query.filter_by(guid=guid, status_id=status.id).first()
        actual = datetime.now()
        if not user != None or actual > user.exp_time:
            return jsonify({'message': 'Datos de activacion invalido'}), 404
        user.status_id = status_activo.id
        db.session.commit()
        user_dict = json.loads(user_schema.dumps(user))
        user_dict['user_datails'] = get_details(user.id)
        user_dict['status'] = get_status(request.json['status_id'])
        user_dict['role'] = get_role(request.json['role_id'])
        user_dict.pop('password')
        db.session.commit()
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
    
@users.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user=Users.query.get(id)
        user_details=UserDetails.query.get(id)
        if user == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        db.session.delete(user_details)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Elemento eliminado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
    
@users.route('/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        user=Users.query.get(id)
        if user == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        
        user.email = request.json['email']
        user.user_name = request.json['user_name']
        user.phone = request.json['phone']
        user.address = request.json['address']
        user.rol_id = request.json['rol_id']
        
        user_dict = json.loads(user_schema.dumps(user))
        user_dict['user_datails'] = get_details(user.id)
        user_dict['status'] = get_status(request.json['status_id'])
        user_dict['role'] = get_role(request.json['role_id'])
        user_dict.pop('password')
        db.session.commit()
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
def get_role(id: int):
    role = Role.query.get(id)
    return json.loads(role_schema.dumps(role))

def get_details(id: int):
    user_details = UserDetails.query.get(id)
    return json.loads(user_details_schema.dumps(user_details))

def get_status(id: int):
    status = UserStatus.query.get(id)
    return json.loads(status_schema.dumps(status))
    