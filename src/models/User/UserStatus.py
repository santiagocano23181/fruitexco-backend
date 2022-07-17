from utils.db import db

class UserStatus(db.Model):
    __tablename__ = 'user_status'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        return "<UserStatus %r>" % self.name