from datetime import datetime, timedelta
import email
from email import message
from itertools import product
from datetime import datetime

from sqlalchemy import text
import math
from flask_cors import cross_origin
from flask import session
import json
import uuid
import jwt
from flask import Blueprint, jsonify, request
from models.User.User import Users
from models.User.UserStatus import UserStatus
from models.User.Role import Role
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db
from utils.ma import ma
from utils.CreateReport import reportePDF
from utils.Templates.Templates import ActivateEmail, RecoverEmail
from utils.email import send_email
from decouple import config
import base64
from os import remove

users = Blueprint("users", __name__)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True


user_schema = UserSchema()
many_user_schema = UserSchema(many=True)


class RoleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


role_schema = RoleSchema()
many_role_schema = RoleSchema(many=True)


class StatusUserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


status_schema = StatusUserSchema()
many_status_schema = StatusUserSchema(many=True)


@users.route("/")
def list_users():
    user = Users.query.all()
    users = json.loads(many_user_schema.dumps(user))
    for u in users:
        u["role"] = get_role(u["role_id"])
        u["status"] = get_status(u["status_id"])
    return jsonify(users)


@users.route("/employees")
def list_employees():
    role = Role.query.filter_by(name="EMPLEADO").first()
    user = Users.query.filter_by(role_id=role.id).all()
    users = json.loads(many_user_schema.dumps(user))
    for u in users:
        u["role"] = get_role(u["role_id"])
        u["status"] = get_status(u["status_id"])
    return jsonify(users)


@users.route("/role/employee", methods=["PATCH"])
def give_employee():
    email = request.json["email"]
    role = Role.query.filter_by(name="EMPLEADO").first()
    user = Users.query.filter_by(email=email).first()
    if user == None:
        return jsonify(messages="El usuario no existe", context=2), 404
    if user.role_id == role.id:
        return jsonify(messages="El usuario ya tiene permisos", context=2), 401
    user.role_id = role.id
    db.session.commit()
    return jsonify(messages="Exito asignando el rol", context=0), 200


@users.route("/role/normal", methods=["PATCH"])
def give_user():
    email = request.json["email"]
    role = Role.query.filter_by(name="USUARIO").first()
    user = Users.query.filter_by(email=email).first()
    if user == None:
        return jsonify(messages="El usuario no existe", context=2), 404
    user.role_id = role.id
    db.session.commit()
    return jsonify(messages="Exito asignando el rol", context=0), 200


@users.route("/profile")
def get_user_by_guid():
    try:
        user_id = session.get("Authorization")
        user = Users.query.get(user_id)
        u = json.loads(user_schema.dumps(user))
        u["role"] = get_role(user.role_id)
        u["status"] = get_status(user.status_id)
        u.pop("password")
        session.pop("Authorization")
        return jsonify(u)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@users.route("/<int:id>")
def get_user(id):
    try:
        user = Users.query.get(id)
        u = json.loads(user_schema.dumps(user))
        u["role"] = get_role(u["role_id"])
        u["status"] = get_status(u["status_id"])
        return jsonify(u)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@users.route("/", methods=["POST"])
def create_user():
    status = UserStatus.query.filter_by(name="INACTIVO").first()
    status_activo = UserStatus.query.filter_by(name="ACTIVO").first()
    status_eliminado = UserStatus.query.filter_by(name="ELIMINADO").first()
    role = Role.query.filter_by(name="USUARIO").first()
    if status == None:
        return (
            jsonify(
                messages="No es posible consultar usuario porque no hay datos en la base de datos",
                context=3,
            ),
            500,
        )
    user = Users.query.filter_by(
        email=request.json["email"], status_id=status_activo.id
    ).first()

    if user != None:
        return jsonify(messages="El usuario ya existe", context=2), 401
    user = Users.query.filter_by(
        email=request.json["email"], status_id=status.id
    ).first()
    if user == None:
        user = Users.query.filter_by(
            email=request.json["email"], status_id=status_eliminado.id
        ).first()
    if user == None:
        new_user = Users(
            request.json["email"],
            request.json["first_name"],
            request.json["second_name"],
            request.json["first_surname"],
            request.json["second_surname"],
            generate_password_hash(request.json["password"], method="sha256"),
            request.json["phone"],
            request.json["address"],
            role.id,
            status.id,
        )
        db.session.add(new_user)
    else:
        actual = datetime.now()
        user.email = request.json["email"]
        user.first_name = request.json["first_name"]
        user.second_name = request.json["second_name"]
        user.first_surname = request.json["first_surname"]
        user.second_surname = request.json["second_surname"]
        user.guid = str(uuid.uuid4())
        user.phone = request.json["phone"]
        user.password = generate_password_hash(
            request.json["password"], method="sha256"
        )
        user.address = request.json["address"]
        user.rol_id = (role.id,)
        user.exp_time = actual + timedelta(minutes=15)
        user.status_id = status.id
    db.session.commit()

    user = Users.query.filter_by(email=request.json["email"]).first()

    user_dict = json.loads(user_schema.dumps(user))
    user_dict.pop("password")

    url = config("FRONT_URL") + "auth/activate/" + user.guid
    activate = ActivateEmail(url)
    email = activate.create_mail()

    send_email("Activar cuenta", email, user.email)

    return (
        jsonify(
            messages="Si la dirección de correo exite, recibira un correo para activar y acceder a su cuenta",
            context=1,
        ),
        200,
    )


@users.route("/login", methods=["POST"])
def login():
    try:
        status = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return (
                jsonify(
                    message="No es posible consultar usuario porque no hay datos en la base de datos",
                    context=3,
                ),
                500,
            )

        user = Users.query.filter_by(
            email=request.json["email"], status_id=status.id
        ).first()

        if user == None:
            return (
                jsonify(messages="Problema al intentar iniciar sesion", context=2),
                404,
            )

        now = datetime.now()
        hours = math.floor((now - user.updated_on) / timedelta(hours=1))

        if user.tries >= 5:
            if hours < 24:
                url = config("FRONT_URL") + "auth/recover/" + user.guid
                user.exp_time = now + timedelta(minutes=15)
                activate = RecoverEmail(url)
                email = activate.create_mail()
                db.session.commit()
                send_email("Recuperar cuenta", email, user.email)
                return (
                    jsonify(
                        messages=f"Se le han acabado los intentos Intentelo en {24 - hours} hora(s)"
                    ),
                    403,
                )

        if hours > 24:
            user.tries = 0
            db.session.commit()

        if not check_password_hash(user.password, request.json["password"]):
            user.updated_on = now
            user.tries = user.tries + 1
            db.session.commit()
            return (
                jsonify(
                    messages="Asegurate que los datos son correctos e intentalo de nuevo"
                ),
                404,
            )

        user.tries = 0
        db.session.commit()
        user_dict = json.loads(user_schema.dumps(user))
        user_dict["status"] = get_status(user.status_id)
        user_dict["role"] = get_role(user.role_id)
        user_dict.pop("password")
        session["user_session"] = user.id
        session["user_rol"] = {"id": user.role_id, "rol": user_dict["role"]}
        actual = datetime.now()
        session["exp_time"] = user.exp_time = actual + timedelta(minutes=15)
        user_dict["id"] = jwt.encode(
            {"id": user_dict["id"]}, config("SECRET_KEY"), algorithm="HS256"
        )
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@users.route("/recover", methods=["POST"])
def recover_user():
    try:
        status = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return (
                jsonify(
                    message="No es posible consultar usuario porque no hay datos en la base de datos",
                    context=3,
                ),
                500,
            )
        user = Users.query.filter_by(
            email=request.json["email"], status_id=status.id
        ).first()
        if user == None:
            return (
                jsonify(
                    messages="Problema al intentar recueprar la contraseña de este usuario",
                    context=2,
                ),
                404,
            )
        actual = datetime.now()

        url = config("FRONT_URL") + "auth/recover/" + user.guid
        user.exp_time = actual + timedelta(minutes=15)
        activate = RecoverEmail(url)
        email = activate.create_mail()

        send_email("Recuperar cuenta", email, user.email)
        db.session.commit()
        return jsonify(messages="Correo de recuperación enviado", context=1), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@users.route("/activate/<guid>", methods=["GET"])
def activate_user(guid):
    try:
        status = UserStatus.query.filter_by(name="INACTIVO").first()
        status_activo = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return (
                jsonify(
                    messages="No es posible consultar usuario porque no hay datos en la base de datos",
                    context=3,
                ),
                500,
            )

        user = Users.query.filter_by(guid=guid, status_id=status.id).first()
        actual = datetime.now()
        if user == None or actual > user.exp_time:
            return jsonify(messages="Datos de activacion invalido", context=3), 404
        user.status_id = status_activo.id
        user.guid = str(uuid.uuid4())
        db.session.commit()
        user_dict = json.loads(user_schema.dumps(user))
        user_dict["status"] = get_status(user.status_id)
        user_dict["role"] = get_role(user.role_id)
        user_dict.pop("password")
        db.session.commit()
        return jsonify(messages="Usuario activado", context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex)), 500


@users.route("/reset/<guid>", methods=["POST"])
def reset_user_password(guid):
    try:
        status = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return (
                jsonify(
                    messages="No es posible consultar usuario porque no hay datos en la base de datos",
                    context=3,
                ),
                500,
            )

        user = Users.query.filter_by(guid=guid, status_id=status.id).first()
        if not user != None:
            return jsonify(messages="Datos de activacion invalido", context=2), 404
        user.password = generate_password_hash(
            request.json["password"], method="sha256"
        )
        user.guid = str(uuid.uuid4())
        user.tries = 0
        user.updated_on = 0
        db.session.commit()
        user_dict = json.loads(user_schema.dumps(user))
        user_dict["status"] = get_status(user.status_id)
        user_dict["role"] = get_role(user.role_id)
        user_dict.pop("password")

        return (
            jsonify(
                messages="Se logro actualizar la cuenta de forma exitosa", context=0
            ),
            200,
        )
    except Exception as ex:
        return jsonify(messages=str(ex)), 500


@users.route("/validate/recover/<guid>", methods=["GET"])
def validate_recover_user(guid):
    try:
        status = UserStatus.query.filter_by(name="ACTIVO").first()
        if status == None:
            return (
                jsonify(
                    messages="No es posible consultar usuario porque no hay datos en la base de datos",
                    context=3,
                ),
                500,
            )

        user = Users.query.filter_by(guid=guid, status_id=status.id).first()
        actual = datetime.now()
        if user == None or actual > user.exp_time:
            return jsonify(messages="Datos de recuperacion invalidos", context=2), 404

        return jsonify(messages="Usuario valido", context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex)), 500


@users.route("/", methods=["DELETE"])
def delete_user():
    try:
        status = UserStatus.query.filter_by(name="ELIMINADO").first()
        id = session.get("Authorization")
        user = Users.query.get(id)
        if user == None:
            return (
                jsonify(
                    messages="No existe un estado el usuario con este ID", context=2
                ),
                404,
            )
        user.status_id = status.id
        db.session.commit()
        return jsonify(messages="Elemento eliminado", context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex)), 500


@users.route("/", methods=["PUT"])
def update_user():
    try:
        id = session.get("Authorization")
        user = Users.query.get(id)
        if user == None:
            return (
                jsonify(
                    messages="No existe un estado el usuario con este ID", context=2
                ),
                404,
            )

        user.first_name = request.json["first_name"]
        user.second_name = request.json["second_name"]
        user.first_surname = request.json["first_surname"]
        user.second_surname = request.json["second_surname"]
        user.email = request.json["email"]
        user.phone = request.json["phone"]
        user.address = request.json["address"]

        user_dict = json.loads(user_schema.dumps(user))
        user_dict["status"] = get_status(user.status_id)
        user_dict["role"] = get_role(user.role_id)
        user_dict.pop("password")
        db.session.commit()
        session.pop("Authorization")
        return jsonify(user_dict), 200
    except Exception as ex:
        return jsonify(messages=str(ex)), 500


@users.route("/password", methods=["PATCH"])
def update_user_pass():
    try:
        id = session.get("Authorization")
        user = Users.query.get(id)
        if user == None:
            return (
                jsonify(
                    messages="No existe un estado el usuario con este ID", context=2
                ),
                404,
            )
        if not check_password_hash(user.password, request.json["password"]):
            return (
                jsonify(
                    messages="Asegurate que los datos son correctos e intentalo de nuevo",
                    context=2,
                ),
                403,
            )
        user.password = generate_password_hash(
            request.json["new_password"], method="sha256"
        )
        user.guid = str(uuid.uuid4())
        db.session.commit()
        session.pop("Authorization")
        return jsonify(messages="Contraseña modificada", context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=2), 500


@users.route("/logout", methods=["DELETE"])
def logout_session():
    id = session.get("Authorization")
    session.pop("user_session", None)
    session.pop("user_rol", None)
    session.pop("exp_time", None)
    return jsonify(messages="Exito al cerrar sesión", context=0), 200


@users.route("/report", methods=["POST"])
def generate_report_user():
    start = request.json["start"]
    finish = request.json["finish"]

    consulta = db.engine.execute(
        text(
            f"""SELECT u.email, (max(u.first_name) || ' ' || max(u.second_name) || ' ' || max(u.first_surname) || ' ' || max(u.second_surname)) as "name", sum(s.total) SUMA_VENTAS
                FROM sales s
                INNER JOIN users u
                ON u.id = s.client_id
                INNER JOIN sale_status ss 
                ON ss.id = s.status_id
                WHERE s.updated_on > '{start}' 
                AND s.updated_on < '{finish}'
                AND (ss."name" = 'PAGADO' OR ss."name" = 'ENVIADO')
                GROUP BY u.email
                ORDER BY SUMA_VENTAS DESC"""
        )
    )
    datos = []
    id_bill = 0
    for row in consulta:
        datos.append(
            {
                "CORREO": row[0],
                "NOMBRE": row[1],
                "VALOR": "$\t{:,.2f}".format(row[2]),
            }
        )
    cabecera = (
        ("CORREO", "CORREO ELECTRONICO"),
        ("DIRECCION", "NOMBRE COMPLETO"),
        ("VALOR", "VALOR DE COMPRAS"),
    )

    titulo = "REPORTE USUARIOS"

    nombrePDF = f"Reporte usuarios {start} - {finish}.pdf"

    reportePDF(
        titulo, cabecera, datos, nombrePDF, None, "{:0>9}".format(id_bill), None
    ).Exportar()
    encoded_string = ""
    with open(nombrePDF, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())

    response = {"name": nombrePDF, "contents": encoded_string.decode("utf-8")}
    remove(nombrePDF)
    return jsonify(response)


def get_role(id: int):
    role = Role.query.get(id)
    return json.loads(role_schema.dumps(role))


def get_status(id: int):
    status = UserStatus.query.get(id)
    return json.loads(status_schema.dumps(status))
