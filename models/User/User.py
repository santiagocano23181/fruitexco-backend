from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from sqlalchemy import event, DDL
import uuid
from utils.db import db
from .Role import Role
from .UserStatus import UserStatus


class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    second_name = db.Column(db.String(45))
    first_surname = db.Column(db.String(45), nullable=False)
    second_surname = db.Column(db.String(45))
    password = db.Column(db.String(200), unique=True, nullable=False)
    exp_time = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tries = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(14), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    
    # Status
    status_id = db.Column(db.Integer, db.ForeignKey('user_status.id'), nullable=False)
    status = db.relationship('UserStatus', 
                             backref='users', 
                             primaryjoin='Users.status_id == UserStatus.id')
    
    def __init__(self, email, first_name, second_name, first_surname, second_surname, password, phone, address, role_id, status_id) -> None:
        actual = datetime.now()
        self.guid = str(uuid.uuid4())
        self.email = email
        self.first_name = first_name
        self.second_name = second_name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.password = password
        self.phone = phone
        self.address = address
        self.created_on = actual
        self.updated_on = actual
        self.tries = 0
        self.exp_time = actual + timedelta(minutes=15)
        self.role_id = role_id
        self.status_id = status_id
    
    def __repr__(self) -> str:
        return '<User %r>' % self.guid
    
event.listen(Role.__table__, 'after_create', DDL('''INSERT INTO role (id, name) VALUES (1, 'ADMINISTRADOR')'''))
event.listen(Role.__table__, 'after_create', DDL('''INSERT INTO role (id, name) VALUES (1, 'ADMINISTRADOR'), (3, 'USUARIO')'''))

event.listen(Users.__table__, 'after_create', DDL(f'''
    INSERT INTO users (id, guid, email, first_name, first_surname, second_surname, password, phone, address, created_on, updated_on, tries, role_id, status_id)
    VALUES (1, '{str(uuid.uuid4())}', 'santiago_cano23181@elpoli.edu.co', 'admin', 'admin', 'admin', '{generate_password_hash('7ru173Xc03DM170NDB', method='sha256')}', '3217443912', 'Calle 106C # 69 - 22', 0, 1, 1)'''))

event.listen(Users.__table__, 'after_create', DDL(f'''
    INSERT INTO users (id, guid, email, first_name, first_surname, second_surname, password, phone, address, created_on, updated_on, tries, role_id, status_id)
    VALUES (2, '{str(uuid.uuid4())}', 'santiagocanoo1811@gmail.com', 'admin', 'admin', 'admin', '{generate_password_hash('4l4pkawa11*', method='sha256')}', '3217443912', 'Calle 106C # 69 - 22', 0, 3, 1)'''))