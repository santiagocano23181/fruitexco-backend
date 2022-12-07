import decimal
from flask import Blueprint, jsonify, request, session
from sqlalchemy import and_, text
from models.Sale.Sale import Sales
from models.Sale.SaleStatus import SaleStatus
from models.Sale.SaleDetail import SaleDetail
from models.Sale.Discount import Discount
from models.Sale.DiscountDetail import DiscountDetail
from models.Sale.Domicile import Domicile
from models.Sale.DomicileDetail import DomicileDetail
from models.User.User import Users
from models.Product.Products import Products
from marshmallow_sqlalchemy.fields import Nested
from utils.CreateReport import reportePDF
from utils.db import db
from utils.ma import ma
from datetime import datetime
import base64
from os import remove

sale = Blueprint("sale", __name__)


class SaleStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleStatus
        include_fk = True


class DomicileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Domicile
        include_fk = True
        load_instance = True


domicile_schema = DomicileSchema()
many_domicile_schema = DomicileSchema(many=True)


class DomicileDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DomicileDetail
        include_fk = True
        load_instance = True

    domicile = Nested(DomicileSchema)


domicile_detail_schema = DomicileDetailSchema()
many_domicile_detail_schema = DomicileDetailSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True
        load_instance = True


user_schema = DomicileDetailSchema()
many_user_schema = DomicileDetailSchema(many=True)


class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        include_fk = True
        load_instance = True

    status = Nested(SaleStatusSchema)
    domicile_detail = Nested(DomicileDetailSchema, many=True)
    client = Nested(UserSchema)


sale_schema = SaleSchema()
many_sale_schema = SaleSchema(many=True)


class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True
        load_instance = True

    status = Nested(SaleSchema)


sale_detail_schema = SaleDetailSchema()
many_sale_detail_schema = SaleDetailSchema(many=True)


@sale.route("/")
def create_sale():
    try:
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )

        domicile = Domicile.query.filter_by(finish_date=None).first()
        if sales == None:
            sales = Sales(id, sale_status.id, 0)
            db.session.add(sales)
            db.session.commit()
        domicile_detail = DomicileDetail.query.filter_by(sale_id=sales.id).first()
        if domicile_detail == None:
            domicile_detail = DomicileDetail(domicile_id=domicile.id, sale_id=sales.id)
            db.session.add(domicile_detail)
            db.session.commit()
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/paid", methods=["PATCH"])
def update_sale_status():
    try:
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sale_status_paid = SaleStatus.query.filter_by(name="PAGADO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        sales.status_id = sale_status_paid.id
        db.session.commit()

        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@sale.route("/domicile_details", methods=["PATCH"])
def update_domicile_details():
    try:
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )

        domicile_detail = DomicileDetail.query.filter_by(sale_id=sales.id).first()
        domicile_detail.address = request.json["address"]
        domicile_detail.phone = request.json["phone"]
        db.session.commit()

        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/actual")
def get_actual():
    try:
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        domicile_detail = DomicileDetail.query.filter(
            DomicileDetail.sale_id == sales.id
        )
        if domicile_detail == None:
            domicile = Domicile.query.filter_by(finish_date=None).first()
            domicile_detail = DomicileDetail(domicile_id=domicile.id, sale_id=sales.id)
            db.session.add(domicile_detail)
            db.session.commit()
        return sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/calculate")
def calculate_actual():
    try:
        addition = 0
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        sale_details = SaleDetail.query.filter(SaleDetail.sale_id == sales.id).all()
        discount = Discount.query.filter_by(finish_date=None).first()

        for sale_detail in sale_details:
            neto = 0
            product = Products.query.get(sale_detail.products_id)
            neto = product.price * sale_detail.cantity
            discount_detail = DiscountDetail.query.filter(
                DiscountDetail.discount_id == discount.id,
                DiscountDetail.sale_details_id == sale_detail.id,
            ).first()
            if discount_detail != None:
                neto = decimal.Decimal(float(neto)) - (
                    decimal.Decimal(float(neto))
                    * (decimal.Decimal(float(discount.amount)) / 100)
                )
            else:
                neto = decimal.Decimal(float(neto))
            addition = addition + neto
        sales.total = addition
        domicile = Domicile.query.filter_by(finish_date=None).first()
        sales.total = sales.total + domicile.price
        db.session.commit()
        return jsonify(addition=addition)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/count")
def count_actual():
    try:
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        if sales == None:
            return jsonify(0)
        sale_count = SaleDetail.query.filter(SaleDetail.sale_id == sales.id).count()
        return jsonify(cantity=sale_count)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/pending")
def get_pending():
    try:
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sales = (
            Sales.query.filter(Sales.status_id != sale_status.id)
            .order_by(Sales.status_id.desc(), Sales.updated_on.desc())
            .all()
        )
        return many_sale_schema.jsonify(sales)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/send", methods=["PATCH"])
def get_pack_off():
    try:
        sale_status = SaleStatus.query.filter_by(name="ENVIADO").first()
        sales_id = request.json["sales"]
        query = db.session.query(Sales).filter(Sales.id.in_(sales_id))
        query.update({Sales.status_id: sale_status.id}, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/bill/<id>")
def generate_bill(id):
    try:
        sale_client = Sales.query.get(id)
        client = sale_client.client
        domicile_detail = DomicileDetail.query.filter_by(sale_id=sale_client.id).first()

        consulta = db.engine.execute(
            text(
                """SELECT s.id ID, (t.name || ' - ' || m.name) as NOMBRE, sd.cantity as CANTIDAD, ((sd.cantity * p.price) - (CASE WHEN dd.id IS NOT NULL THEN (sd.cantity * p.price) * (d.amount / 100) ELSE 0 END)) as PRECIO, s.total as TOTAL
                        FROM sales s 
                        INNER JOIN sale_details sd 
                        ON s.id = sd.sale_id
                        INNER JOIN products p
                        ON sd.products_id = p.id
                        INNER JOIN mesure m
                        ON p.mesure_id = m.id
                        INNER JOIN taste t
                        ON t.id = p.taste_id
                        LEFT JOIN discount_details dd
                        ON dd.sale_details_id = sd.id
                        LEFT JOIN discount d 
                        ON d.id = dd.discount_id"""
            )
        )
        datos = []
        total = 0
        id_bill = 0
        for row in consulta:
            datos.append(
                {
                    "NOMBRE": row[1],
                    "CANTIDAD": row[2],
                    "PRECIO": "$\t{:,.2f}".format(row[3]),
                }
            )
            id_bill = row[0]
            total = "${:,.2f}".format(row[4])
        datos.append(
            {
                "NOMBRE": "Domicilio",
                "CANTIDAD": 1,
                "PRECIO": "$\t{:,.2f}".format(domicile_detail.domicile.price),
            }
        )
        cabecera = (
            ("NOMBRE", "NOMBRE PRODUCTO"),
            ("CANTIDAD", "CANTIDAD"),
            ("PRECIO", "COSTO"),
        )

        titulo = "FACTURA"

        cliente = {
            "Nombre": client.first_name
            + " "
            + ((client.second_name + " ") if client.second_name != None else "")
            + client.first_surname
            + " "
            + ((client.second_surname + " ") if client.second_surname != None else ""),
            "Dirección": domicile_detail.address,
            "Teléfono": domicile_detail.phone,
        }

        nombrePDF = f"Factura {'{:0>9}'.format(1)} - {str(datetime.now()).replace(':', '_').replace('.', '_')}.pdf"

        reportePDF(
            titulo, cabecera, datos, nombrePDF, cliente, "{:0>9}".format(id_bill), total
        ).Exportar()
        encoded_string = ""
        with open(nombrePDF, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())

        response = {"name": nombrePDF, "contents": encoded_string.decode("utf-8")}
        remove(nombrePDF)
        return jsonify(response)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale.route("/report", methods=["POST"])
def generate_report_sale():
    try:
        start = request.json['start']
        finish = request.json['finish']

        consulta = db.engine.execute(
            text(
                f"""SELECT u.email, u.address, s.total, to_char(s.updated_on, 'DD/MM/YYYY HH24:MI:SS') as date, (select sum(total) FROM sales s WHERE s.updated_on > '2022-11-10' and s.updated_on < '2022-12-05') total
                    FROM sales s
                    INNER JOIN users u
                    ON u.id = s.client_id
                    INNER JOIN sale_status ss 
                    ON ss.id = s.status_id
                    WHERE s.updated_on > '{start}' 
                    AND s.updated_on < '{finish}' 
                    AND (ss."name" = 'PAGADO' OR ss."name" = 'ENVIADO')"""
            )
        )
        datos = []
        total = 0
        id_bill = 0
        for row in consulta:
            datos.append(
                {
                    "CORREO": row[0],
                    "DIRECCION": row[1],
                    "VALOR": "$\t{:,.2f}".format(row[2]),
                    "FECHA": row[3],
                }
            )
            total = "${:,.2f}".format(row[4])
        cabecera = (
            ("CORREO", "CORREO ELECTRONICO"),
            ("DIRECCION", "DIRECCION ENVIO"),
            ("VALOR", "VALOR VENTA"),
            ("FECHA", "FECHA ACTUALIZACIÓN"),
        )

        titulo = "REPORTE VENTAS"

        nombrePDF = (
            f"Reporte ventas {start} - {finish}.pdf"
        )

        reportePDF(
            titulo, cabecera, datos, nombrePDF, None, "{:0>9}".format(id_bill), total
        ).Exportar()
        encoded_string = ""
        with open(nombrePDF, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())

        response = {"name": nombrePDF, "contents": encoded_string.decode("utf-8")}
        remove(nombrePDF)
        return jsonify(response)
    except Exception as ex:
            return jsonify(messages=str(ex), context=3), 500
