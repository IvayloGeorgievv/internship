from flask import Blueprint, request, jsonify
from services.establishment_service import (
    get_all_establishments,
    get_establishment_by_id,
    create_establishment,
    update_establishment,
    delete_establishment
)
from utils.auth import require_api_key

establishments_bp = Blueprint('establishments', __name__)

@establishments_bp.route('/', methods=['GET'], endpoint='get_establishments')
@require_api_key
def get_establishments():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    sort_by = request.args.get('sort_by', 'name', type=str)
    order = request.args.get('order', 'ASC', type=str)

    establishments = get_all_establishments(page, page_size, sort_by, order)
    return jsonify(establishments)

@establishments_bp.route('/<int:id>', methods=['GET'], endpoint='get_establishment')
@require_api_key
def get_establishment(id):
    establishment = get_establishment_by_id(id)
    if establishment:
        return jsonify(establishment)
    return jsonify({'error': 'Establishment not found'}), 404

@establishments_bp.route('/', methods=['POST'], endpoint='add_establishment')
@require_api_key
def add_establishment():
    data = request.get_json()
    if create_establishment(data):
        return jsonify({'message': 'Establishment created'}), 201
    return jsonify({'error': 'Failed to create establishment'}), 400

@establishments_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_establishment')
@require_api_key
def modify_establishment(id):
    data = request.get_json()
    if update_establishment(id, data):
        return jsonify({'message': 'Establishment updated'})
    return jsonify({'error': 'Failed to update establishment'}), 400

@establishments_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_establishment')
@require_api_key
def remove_establishment(id):
    if delete_establishment(id):
        return jsonify({'message': 'Establishment deleted'})
    return jsonify({'error': 'Failed to delete establishment'}), 400
