from utils.db import db

class SaleStatus(db.Model):
    __tablename__ = 'sale_status'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return "<SaleStatus %r>" % self.name