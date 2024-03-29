from utils.db import db
from .Domicile import Domicile
from .Sale import Sales


class DomicileDetail(db.Model):
    __tablename__ = "domicile_details"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(14))

    # Sale
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"))
    sale = db.relationship("Sales", back_populates="domicile_detail", lazy=True)

    # Domicile
    domicile_id = db.Column(db.Integer, db.ForeignKey("domicile.id"))
    domicile = db.relationship(
        "Domicile", backref=db.backref("domicile_detail", lazy=True)
    )

    def __init__(self, domicile_id, sale_id) -> None:
        self.domicile_id = domicile_id
        self.sale_id = sale_id

    def __repr__(self) -> str:
        return "<DomicileDetail %r>" % self.address
