from datetime import datetime
from utils.db import db

class Domicile(db.Model):
    __tablename__ = 'domicile'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finish_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self) -> str:
        return "<Domicile %r>" % self.price