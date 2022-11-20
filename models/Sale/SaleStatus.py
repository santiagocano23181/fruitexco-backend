from sqlalchemy import event, DDL
from utils.db import db


class SaleStatus(db.Model):
    __tablename__ = 'sale_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return '<SaleStatus %r>' % self.name

event.listen(SaleStatus.__table__, 'after_create', DDL('''INSERT INTO sale_status (id, name) VALUES (1, 'EN CARRITO'), (2, 'PAGADO'), (3, 'CANCELADO')'''))
