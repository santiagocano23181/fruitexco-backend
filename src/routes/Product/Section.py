from itertools import product
import json
from flask import Blueprint, jsonify, request
from models.Product.Section import Section
from models.Product.Products import Products
from models.Product.ProductStatus import ProductStatus
from models.Product.Mesure import Mesure
from models.Product.Taste import Taste
from marshmallow_sqlalchemy.fields import Nested
from utils.db import db
from utils.ma import ma
from sqlalchemy.orm import joinedload, session
from sqlalchemy import and_

section = Blueprint('section', __name__)


class MesureSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


mesure_schema = MesureSchema()
many_status_schema = MesureSchema(many=True)


class TasteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


taste_schema = TasteSchema()
many_taste_schema = TasteSchema(many=True)


class StatusProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


status_schema = StatusProductSchema()
many_status_schema = StatusProductSchema(many=True)


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        include_fk = True
        load_instance = True
    mesure = Nested(MesureSchema)
    taste = Nested(TasteSchema)
    status = Nested(StatusProductSchema)


product_schema = ProductSchema()
many_product_schema = ProductSchema(many=True)


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        include_fk = True
        load_instance = True
    products = Nested(ProductSchema, many=True)


section_schema = SectionSchema()
many_section_schema = SectionSchema(many=True)


@section.route('/')
def list_section():
    try:
        sections = Section.query.all()
        section_json = json.loads(many_section_schema.dumps(sections))
        status_activo = ProductStatus.query.filter_by(name='ACTIVO').first()
        for sec in section_json:
            product = Products.query.filter(and_(Products.section_id == sec['id'], Products.status_id == status_activo.id)).distinct(
                Products.taste_id).limit(4).all()
            sec['products'] = json.loads(many_product_schema.dumps(product))
        return jsonify(section_json)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@section.route('/', methods=['POST'])
def create_section():
    try:
        new_section = Section(request.json['name'])
        print(new_section)
        db.session.add(new_section)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@section.route('/<id>', methods=['PUT'])
def update_section(id):
    try:
        section = Section.query.get(id)
        if section == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        section.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@section.route('/<id>')
def get_section(id):
    try:
        status_activo = ProductStatus.query.filter_by(name='ACTIVO').first()
        sections = Section.query.get(id)
        section_json = json.loads(section_schema.dumps(sections))
        product = Products.query.filter(and_(
            Products.section_id == section_json['id'], Products.status_id == status_activo.id)).distinct(Products.taste_id).all()
        section_json['products'] = json.loads(many_product_schema.dumps(product))
        return jsonify(section_json)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
