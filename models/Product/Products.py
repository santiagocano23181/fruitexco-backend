from datetime import datetime
from utils.db import db
from .Mesure import Mesure
from .Taste import Taste
from .ProductStatus import ProductStatus

class Products(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    photo = db.Column(db.String(300))
    
    #mesure
    mesure_id = db.Column(db.Integer, db.ForeignKey('mesure.id'),nullable=False)
    mesure = db.relationship('Mesure', back_populates='products')
    
    #taste
    taste_id = db.Column(db.Integer, db.ForeignKey('taste.id'),nullable=False)
    taste = db.relationship('Taste', back_populates='products')
    
    #status
    status_id = db.Column(db.Integer, db.ForeignKey('product_status.id'),nullable=False)
    status = db.relationship('ProductStatus', back_populates='products')

    #section
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', back_populates='products')
    
    def __init__(self, price, photo, mesure_id, taste_id, status_id, section_id) -> None:
        self.price = price
        self.created_on = datetime.now()
        self.photo = photo
        self.mesure_id = mesure_id
        self.taste_id = taste_id
        self.status_id = status_id
        self.section_id = section_id
    
    def __repr__(self) -> str:
        return '<Products %r>' % self.price