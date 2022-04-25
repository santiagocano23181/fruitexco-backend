from flask import Blueprint, jsonify

main=Blueprint('product_blueprint', __name__)

@main.route('/')
def get_products():
    return jsonify({'message': 'try'})