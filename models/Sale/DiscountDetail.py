from utils.db import db
from .Discount import Discount
from .Sale import Sales

class DiscountDetail(db.Model):
    __tablename__ = 'discount_details'
    
    id = db.Column(db.Integer, primary_key=True)
    
    #Discount
    discount_id = db.Column(db.Integer,  db.ForeignKey('discount.id'))
    discount = db.relationship('Discount', backref=db.backref('discount_details', lazy=True))
    
    #Sale details
    sale_details_id = db.Column(db.Integer,  db.ForeignKey('sale_details.id'))
    sale_details = db.relationship('SaleDetail' , back_populates = 'discount_detail', lazy = True)

    def __init__(self, discount_id, sale_details_id) -> None:
        self.discount_id = discount_id
        self.sale_details_id = sale_details_id
    
    def __repr__(self) -> str:
        return '<DiscountDetail %r>' % self.address