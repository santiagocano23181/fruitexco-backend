from datetime import datetime
from utils.db import db

class Discount(db.Model):
    __tablename__ = 'discount'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finish_date = db.Column(db.DateTime)
    
    def __repr__(self) -> str:
        return "<Discount %r>" % self.amount