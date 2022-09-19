from datetime import datetime
from utils.db import db

class Discount(db.Model):
    __tablename__ = 'discount'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finish_date = db.Column(db.DateTime)
    needed = db.Column(db.Numeric, nullable=True)

    def __init__(self, amount, needed) -> None:
        actual = datetime.now()
        self.amount = amount
        self.needed = needed
        self.start_date = actual
    
    def __repr__(self) -> str:
        return "<Discount %r>" % self.amount