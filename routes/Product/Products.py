import json
from flask import Blueprint, jsonify, request
from sqlalchemy import or_, text
from marshmallow_sqlalchemy.fields import Nested
from models.Product.Products import Products
from models.Product.Mesure import Mesure
from models.Product.Taste import Taste
from models.Product.ProductStatus import ProductStatus
from models.Product.Section import Section
from utils.db import db
from utils.ma import ma
from sqlalchemy import and_
import base64
from os import remove
from utils.CreateReport import reportePDF

products = Blueprint('products', __name__)


class MesureSchema(ma.Schema):
    class Meta:
        fields = ('id','name')

mesure_schema = MesureSchema()
many_status_schema = MesureSchema(many=True)

class TasteSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
taste_schema = TasteSchema()
many_taste_schema = TasteSchema(many=True)

class StatusProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name')
        
status_schema = StatusProductSchema()
many_status_schema = StatusProductSchema(many=True)

class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description')
        
section_schema = SectionSchema()
many_section_schema = SectionSchema(many=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        include_fk = True
        load_instance = True
    mesure = Nested(MesureSchema)
    taste = Nested(TasteSchema)
    section=Nested(SectionSchema)
    status=Nested(StatusProductSchema)
        
product_schema = ProductSchema()
many_product_schema = ProductSchema(many=True)

@products.route('/')
def list_products():
    try:
        status = ProductStatus.query.filter_by(name='INACTIVO').first()
        status_activo = ProductStatus.query.filter_by(name='ACTIVO').first()
        product = Products.query.filter(or_(Products.status_id == status.id, Products.status_id == status_activo.id))
        products_json = json.loads(many_product_schema.dumps(product))
        return jsonify(products_json)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500

@products.route('/<int:id>')
def get_product(id):
    try:
        product = Products.query.get(id)
        p = json.loads(product_schema.dumps(product))
        p['mesure'] = get_mesure(p['mesure_id'])
        p['taste'] = get_taste(p['taste_id'])
        p['status'] = get_status(p['status_id'])
        p['section'] = get_section(p['section_id'])
        return jsonify(p)
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@products.route('/', methods=['POST'])
def create_products():
    try:
        if request.json['mesure_id'] == 'otro':
            mesure = Mesure.query.filter_by(name=str(request.json['mesure']['name']).upper()).first()
            if mesure == None:
                new_mesure = Mesure(str(request.json['mesure']['name']).upper())
                db.session.add(new_mesure)
                db.session.commit()
                mesure = new_mesure
                request.json['mesure'] = json.loads(mesure_schema.dumps(mesure))
        else:
            mesure = Mesure.query.get(request.json['mesure_id'])
        if request.json['taste_id'] == 'otro':
            taste = Taste.query.filter_by(name=str(request.json['taste']['name']).upper()).first()
            if taste == None:
                new_taste = Taste(str(request.json['taste']['name']).upper())
                db.session.add(new_taste)
                db.session.commit()
                taste = new_taste
                request.json['taste'] = json.loads(taste_schema.dumps(taste))
        else:
            taste = Taste.query.get(request.json['taste_id'])
        new_product = Products(request.json['price'],
                               request.json['photo'],
                               mesure.id,
                               taste.id,
                               request.json['status_id'],
                               request.json['section_id'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify(messages='Elemento creado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=5), 500
    
@products.route('/<id>', methods=['DELETE'])
def delete_products(id):
    try:
        status = ProductStatus.query.filter_by(name='RETIRADO').first()
        product=Products.query.get(id)
        if product == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        product.status_id = status.id
        db.session.commit()
        return jsonify(messages='Elemento eliminado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=3), 500
    
@products.route('/<id>', methods=['PUT'])
def update_product(id):
    try:
        product=Products.query.get(id)
        if product == None:
            return jsonify(messages='No existe un estado el usuario con este ID', context=2), 404
        if request.json['mesure_id'] == 'otro':
            mesure = Mesure.query.filter_by(name=str(request.json['mesure']['name']).upper()).first()
            if mesure == None:
                new_mesure = Mesure(str(request.json['mesure']['name']).upper())
                db.session.add(new_mesure)
                db.session.commit()
                mesure = new_mesure
                request.json['mesure'] = json.loads(mesure_schema.dumps(mesure))
        else:
            mesure = Mesure.query.get(request.json['mesure_id'])
        if request.json['taste_id'] == 'otro':
            taste = Taste.query.filter_by(name=str(request.json['taste']['name']).upper()).first()
            if taste == None:
                new_taste = Taste(str(request.json['taste']['name']).upper())
                db.session.add(new_taste)
                db.session.commit()
                taste = new_taste
                request.json['taste'] = json.loads(taste_schema.dumps(taste))
        else:
            taste = Taste.query.get(request.json['taste_id'])
        product.price = request.json['price']
        product.photo = request.json['photo']
        product.mesure_id = mesure.id
        product.taste_id = taste.id
        product.status_id = request.json['status_id']
        product.section_id = request.json['section_id']
        
        db.session.commit()
        return jsonify(messages='Elemento actualizado', context=0), 200
    except Exception as ex:
        return jsonify(messages=str(ex), context=5), 500
    
@products.route('/taste/<id>', methods=['GET'])
def get_products_by_taste_id(id):
    try:
        status_activo = ProductStatus.query.filter_by(name='ACTIVO').first()
        product = Products.query.filter(and_(Products.taste_id==id, Products.status_id==status_activo.id)).all()
        products_json = json.loads(many_product_schema.dumps(product))
        return jsonify(products_json)
    except Exception as ex:
        return jsonify(messages=str(ex), context=5), 500
    
    
@products.route("/report", methods=["POST"])
def generate_report_sale():
    try:
        start = request.json['start']
        finish = request.json['finish']

        consulta = db.engine.execute(
            text(
                f"""
                    SELECT (MAX(t.name) || ' - ' || MAX(m.name)) as NOMBRE, SUM(sd.cantity) as VENDIDO
                    FROM sales s
                    INNER JOIN sale_status ss 
                    ON ss.id = s.status_id
                    INNER JOIN sale_details sd
                    ON sd.sale_id = s.id
                    INNER JOIN products p 
                    ON p.id = sd.products_id
                    INNER JOIN mesure m 
                    ON m.id = p.mesure_id
                    INNER JOIN taste t 
                    ON t.id = p.taste_id
                    WHERE s.updated_on > '{start}' 
                    AND s.updated_on < '{finish}' 
                    AND (ss."name" = 'PAGADO' OR ss."name" = 'ENVIADO')
                    GROUP BY p.id
                    ORDER BY VENDIDO DESC"""
            )
        )
        datos = []
        total = 0
        id_bill = 0
        for row in consulta:
            datos.append(
                {
                    "NOMBRE": row[0],
                    "VENDIDO": row[1],
                }
            )
        cabecera = (
            ("NOMBRE", "NOMBRE DEL PRODUCTO"),
            ("VENDIDO", "CANTIDAD VENDIDA"),
        )

        titulo = "REPORTE PRODUCTOS"

        nombrePDF = (
            f"Reporte productos {start} - {finish}.pdf"
        )

        reportePDF(
            titulo, cabecera, datos, nombrePDF, None, "{:0>9}".format(id_bill), None
        ).Exportar()
        encoded_string = ""
        with open(nombrePDF, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())

        response = {"name": nombrePDF, "contents": encoded_string.decode("utf-8")}
        remove(nombrePDF)
        return jsonify(response)
    except Exception as ex:
            return jsonify(messages=str(ex), context=3), 500


def get_mesure(id: int):
    mesure = Mesure.query.get(id)
    return json.loads(mesure_schema.dumps(mesure))

def get_taste(id: int):
    taste = Taste.query.get(id)
    return json.loads(taste_schema.dumps(taste))

def get_status(id: int):
    status = ProductStatus.query.get(id)
    return json.loads(status_schema.dumps(status))
    
def get_section(id: int):
    section = Section.query.get(id)
    return json.loads(section_schema.dumps(section))