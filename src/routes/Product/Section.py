import json
from flask import Blueprint, jsonify, request
from models.Product.Section import Section
from utils.db import db
from utils.ma import ma

section = Blueprint('section', __name__)

class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description')
        
section_schema = SectionSchema()
many_sections_schema = SectionSchema(many=True)

@section.route('/')
def list_section():
    try:
        sections = Section.query.all()
        return many_sections_schema.jsonify(sections)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@section.route('/new', methods=['PUT'])
def create_section():
    try:
        new_section = Section(request.json['name'])
        print(new_section)
        db.session.add(new_section)
        db.session.commit()
        return jsonify({'message': 'Elemento creado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@section.route('/update/<id>', methods=['PUT'])
def update_section(id):
    try:
        section=Section.query.get(id)
        if section == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        section.name = request.json['name']
        db.session.commit()
        return jsonify({'message': 'Elemento actualizado'}), 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
    
@section.route('/get/<id>')
def get_section(id):
    try:
        section=Section.query.get(id)
        if section == None:
            return jsonify({'message': 'No existe un estado el usuario con este ID'}), 404
        return section_schema.jsonify(section)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500