from flask import Blueprint, request, jsonify
from services.sale_service import (
    get_all_sales,
    get_sale_by_id,
    create_sale,
    update_sale,
    delete_sale
)
from utils.auth import require_api_key

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['GET'], endpoint='get_sales')
@require_api_key
def get_sales():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    sort_by = request.args.get('sort_by', 'sale_date', type=str)
    order = request.args.get('order', 'DESC', type=str)

    filters = {}
    for key in request.args:
        if key not in ['page', 'page_size', 'sort_by', 'order']:
            filters[key] = request.args.getlist(key)

    sales = get_all_sales(page, page_size, sort_by, order, filters)
    return jsonify(sales)

@sales_bp.route('/<int:id>', methods=['GET'], endpoint='get_sale')
@require_api_key
def get_sale(id):
    sale = get_sale_by_id(id)
    if sale:
        return jsonify(sale)
    return jsonify({'error': 'Sale not found'}), 404

@sales_bp.route('/', methods=['POST'], endpoint='add_sale')
@require_api_key
def add_sale():
    data = request.get_json()
    if create_sale(data):
        return jsonify({'message': 'Sale created'}), 201
    return jsonify({'error': 'Failed to create sale'}), 400

@sales_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_sale')
@require_api_key
def modify_sale(id):
    data = request.get_json()
    if update_sale(id, data):
        return jsonify({'message': 'Sale updated'})
    return jsonify({'error': 'Failed to update sale'}), 400

@sales_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_sale')
@require_api_key
def remove_sale(id):
    if delete_sale(id):
        return jsonify({'message': 'Sale deleted'})
    return jsonify({'error': 'Failed to delete sale'}), 400
