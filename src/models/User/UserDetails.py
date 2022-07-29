from utils.db import db
from .User import Users

class UserDetails(db.Model):
    __tablename__ = 'user_details'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False, primary_key=True)
    user = db.relationship('Users', backref=db.backref('user_details', lazy=True))
    first_name = db.Column(db.String(45))
    second_name = db.Column(db.String(45))
    first_surname = db.Column(db.String(45))
    second_surname = db.Column(db.String(45))
    
    def __init__(self, id) -> None:
        self.user_id = id
    
    def __repr__(self) -> str:
        return "<UserStatus %r>" % self.first_name