from utils.db import db
from .Feature import Feature

feature_taste = db.Table('feature_taste',
    db.Column('taste_id', db.Integer, db.ForeignKey('taste.id'), primary_key=True),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True)
)

class Taste(db.Model):
    __tablename__ = 'taste'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship("Products", back_populates="taste")
    
    def __init__(self, name) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return "<Taste %r>" % self.name