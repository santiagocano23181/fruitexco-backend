from utils.db import db
from .Domicile import Domicile
from .Sale import Sales

class SaleDetail(db.Model):
    __tablename__ = 'sale_details'
    
    address = db.Column(db.String(100))
    phone = db.Column(db.String(14))
    
    #Sale
    sale_id = db.Column(db.Integer,  db.ForeignKey('sales.id'), primary_key=True)
    sale = db.relationship('Sales', backref=db.backref('sale_detail', lazy=True))
    
    #Domicile
    sale_id = db.Column(db.Integer,  db.ForeignKey('domicile.id'), primary_key=True)
    sale = db.relationship('Domicile', backref=db.backref('sale_detail', lazy=True))
    
    def __repr__(self) -> str:
        return "<SaleDetail %r>" % self.address