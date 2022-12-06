import json
from flask import Blueprint, jsonify, request, session
from sqlalchemy import and_
from models.Product.Products import Products
from models.Sale.Discount import Discount
from models.Sale.DiscountDetail import DiscountDetail
from models.Sale.Domicile import Domicile
from models.Sale.SaleDetail import SaleDetail
from models.Sale.SaleStatus import SaleStatus
from models.Sale.Sale import Sales
from marshmallow_sqlalchemy.fields import Nested
from utils.db import db
from utils.ma import ma

sale_detail = Blueprint("sale_detail", __name__)


class MesureSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


mesure_schema = MesureSchema()
many_status_schema = MesureSchema(many=True)


class TasteSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


taste_schema = TasteSchema()
many_taste_schema = TasteSchema(many=True)


class StatusProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


status_schema = StatusProductSchema()
many_status_schema = StatusProductSchema(many=True)


class SectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description")


section_schema = SectionSchema()
many_section_schema = SectionSchema(many=True)


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        include_fk = True
        load_instance = True

    mesure = Nested(MesureSchema)
    taste = Nested(TasteSchema)
    section = Nested(SectionSchema)
    status = Nested(StatusProductSchema)


class DiscountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discount
        include_fk = True
        load_instance = True


discount_schema = DiscountSchema()
many_discount_schema = DiscountSchema(many=True)


class DiscountDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DiscountDetail
        include_fk = True
        load_instance = True

    discount = Nested(DiscountSchema)


discount_detail_schema = DiscountDetailSchema()
many_discount_detail_schema = DiscountDetailSchema(many=True)


class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True
        load_instance = True

    products = Nested(ProductSchema)
    discount_detail = Nested(DiscountDetailSchema, many=True)


sale_detail_schema = SaleDetailSchema()
many_sale_detail_schema = SaleDetailSchema(many=True)


@sale_detail.route("/", methods=["POST"])
def create_sale_detail():
    try:
        client_id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sale = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == client_id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        sale_details = SaleDetail.query.filter(
            and_(
                SaleDetail.sale_id == sale.id,
                SaleDetail.products_id == request.json["product_id"],
            )
        ).first()
        if sale_details == None:
            sale_details = SaleDetail(
                sale.id, request.json["product_id"], request.json["cantity"]
            )
            db.session.add(sale_details)
        else:
            sale_details.cantity = sale_details.cantity + request.json["cantity"]
        discount = Discount.query.filter_by(finish_date=None).first()
        discount_detail = DiscountDetail.query.filter(
            and_(
                DiscountDetail.discount_id == discount.id,
                DiscountDetail.sale_details_id == sale_details.id,
            )
        ).first()
        if discount_detail == None:
            if discount.needed <= request.json["cantity"]:
                discount_detail = DiscountDetail(discount.id, sale_details.id)
                db.session.add(discount_detail)
        db.session.commit()
        return sale_detail_schema.jsonify(sale_details)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale_detail.route("/")
def get_sale_detail():
        id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sale = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        sale_details = SaleDetail.query.filter(SaleDetail.sale_id == sale.id).all()

        return many_sale_detail_schema.jsonify(sale_details)


@sale_detail.route("/<id>")
def get_sale_detail_by_sale_id(id):
    try:
        sale = Sales.query.get(id)
        sale_details = SaleDetail.query.filter(SaleDetail.sale_id == sale.id).all()

        return many_sale_detail_schema.jsonify(sale_details)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500


@sale_detail.route("/cantity/<id>", methods=["PATCH"])
def update_cantity_sale_detail(id):
    sale_details = SaleDetail.query.get(id)
    sale_details.cantity = request.json["cantity"]

    discount = Discount.query.filter_by(finish_date=None).first()
    db.session.add(sale_details)

    discount_detail = DiscountDetail.query.filter(
        and_(
            DiscountDetail.discount_id == discount.id,
            DiscountDetail.sale_details_id == sale_details.id,
        )
    ).first()
    if discount.needed <= request.json["cantity"]:
        if discount_detail == None:
            discount_detail = DiscountDetail(discount.id, sale_details.id)
            db.session.add(discount_detail)
    else:
        if discount_detail != None:
            db.session.delete(discount_detail)
    db.session.commit()
    return sale_detail_schema.jsonify(sale_detail)


@sale_detail.route("/<id>", methods=["DELETE"])
def delete_sale_detail(id):
    try:
        user_id = session.get("Authorization")
        sale_status = SaleStatus.query.filter_by(name="EN CARRITO").first()
        sale = (
            Sales.query.filter(
                and_(Sales.status_id == sale_status.id, Sales.client_id == user_id)
            )
            .order_by(Sales.created_on)
            .first()
        )
        sale_details = SaleDetail.query.get(id)

        discount = Discount.query.filter_by(finish_date=None).first()

        discount_detail = DiscountDetail.query.filter(
            and_(
                DiscountDetail.discount_id == discount.id,
                DiscountDetail.sale_details_id == sale_details.id,
            )
        ).first()
        if discount_detail != None:
            db.session.delete(discount_detail)
        db.session.delete(sale_details)
        db.session.commit()
        return sale_detail_schema.jsonify(sale_detail)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500

