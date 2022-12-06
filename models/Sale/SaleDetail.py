from utils.db import db
from ..Product.Products import Products
from .Sale import Sales

class SaleDetail(db.Model):
    __tablename__ = 'sale_details'
    
    id = db.Column(db.Integer, primary_key=True)
    cantity = db.Column(db.Float)
    
    #Sale
    sale_id = db.Column(db.Integer,  db.ForeignKey('sales.id'))
    sale = db.relationship('Sales', backref=db.backref('sale_details', lazy=True))
    
    #Products
    products_id = db.Column(db.Integer,  db.ForeignKey('products.id'))
    products = db.relationship('Products', backref=db.backref('sale_details', lazy=True))
    
    discount_detail = db.relationship('DiscountDetail', back_populates = 'sale_details', lazy = True)

    def __init__(self, sale_id, products_id, cantity) -> None:
        self.sale_id = sale_id
        self.products_id = products_id
        self.cantity = cantity
    
    def __repr__(self) -> str:
        return '<SaleDetail %r>' % self.cantity