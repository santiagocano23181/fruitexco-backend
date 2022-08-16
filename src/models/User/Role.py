from sqlalchemy import event, DDL
from utils.db import db


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return "<Role %r>" % self.name

event.listen(Role.__table__, 'after_create', DDL("""INSERT INTO role (id, name) VALUES (1, 'ADMINISTRADOR'), (2, 'EMPLEADO'), (3, 'USUARIO')"""))