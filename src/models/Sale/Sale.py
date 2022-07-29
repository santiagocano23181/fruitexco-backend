from datetime import datetime
from utils.db import db
from ..User.User import Users
from .SaleStatus import SaleStatus

class Sales(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Numeric)
    
    # Client
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client = db.relationship('Users', backref=db.backref('Sales', lazy=True))
    
    # Status
    client_id = db.Column(db.Integer, db.ForeignKey('sale_status.id'), nullable=False)
    client = db.relationship('SaleStatus', backref=db.backref('Sales', lazy=True))
    
    def __repr__(self) -> str:
        return "<Sales %r>" % self.name