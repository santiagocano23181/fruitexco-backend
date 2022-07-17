from utils.db import db

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return "<Role %r>" % self.name
    