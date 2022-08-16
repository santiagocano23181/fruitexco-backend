from sqlalchemy import event, DDL
from utils.db import db


class ProductStatus(db.Model):
    __tablename__ = 'product_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return "<ProductStatus %r>" % self.name

event.listen(ProductStatus.__table__, 'after_create', DDL("""INSERT INTO product_status (id, name) VALUES (1, 'ACTIVO'), (2, 'INACTIVO'), (3, 'RETIRADO')"""))
