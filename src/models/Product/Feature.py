from utils.db import db


class Feature(db.Model):
    __tablename__ = 'feature'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    
    def __init__(self, name) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return "<Feature %r>" % self.name