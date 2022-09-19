from utils.db import db

class Section(db.Model):
    __tablename__ = 'section'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    description = db.Column(db.String(45), unique=True, nullable=False)
    
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description
    
    def __repr__(self) -> str:
        return "<Mesure %r>" % self.name