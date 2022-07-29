from datetime import datetime, timedelta
import uuid
from utils.db import db
from .Role import Role
from .UserStatus import UserStatus


class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_name = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    exp_time = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    phone = db.Column(db.String(14), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    
    # Role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    
    # Status
    status_id = db.Column(db.Integer, db.ForeignKey('user_status.id'), nullable=False)
    status = db.relationship('UserStatus', 
                             backref='users', 
                             primaryjoin="Users.status_id == UserStatus.id")
    
    def __init__(self, email, user_name, password, phone, address, role_id, status_id) -> None:
        actual = datetime.now()
        self.guid = str(uuid.uuid4())
        self.email = email
        self.user_name = user_name
        self.password = password
        self.phone = phone
        self.address = address
        self.created_on = actual
        self.exp_time = actual + timedelta(minutes=15)
        self.role_id = role_id
        self.status_id = status_id
    
    def __repr__(self) -> str:
        return "<User %r>" % self.guid