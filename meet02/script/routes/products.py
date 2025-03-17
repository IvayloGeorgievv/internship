from flask import Blueprint, request, jsonify
from services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)
from utils.auth import require_api_key

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'], endpoint='get_products')
@require_api_key
def get_products():
    products = get_all_products()
    return jsonify(products)

@products_bp.route('/<int:id>', methods=['GET'], endpoint='get_product')
@require_api_key
def get_product(id):
    product = get_product_by_id(id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@products_bp.route('/', methods=['POST'], endpoint='add_product')
@require_api_key
def add_product():
    data = request.get_json()
    if create_product(data):
        return jsonify({'message': 'Product created'}), 201
    return jsonify({'error': 'Failed to create product'}), 400

@products_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_product')
@require_api_key
def modify_product(id):
    data = request.get_json()
    if update_product(id, data):
        return jsonify({'message': 'Product updated'})
    return jsonify({'error': 'Failed to update product'}), 400

@products_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_product')
@require_api_key
def remove_product(id):
    if delete_product(id):
        return jsonify({'message': 'Product deleted'})
    return jsonify({'error': 'Failed to delete product'}), 400
