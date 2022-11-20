from utils.db import db

class Mesure(db.Model):
    __tablename__ = 'mesure'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    products = db.relationship('Products', back_populates='mesure')
    
    def __init__(self, name) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return '<Mesure %r>' % self.name