from flask import Blueprint, request, jsonify
from services.promotion_service import (
    get_all_promotions,
    get_promotion_by_id,
    create_promotion,
    update_promotion,
    delete_promotion
)
from utils.auth import require_api_key

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/', methods=['GET'], endpoint='get_promotions')
@require_api_key
def get_promotions():
    promotions = get_all_promotions()
    return jsonify(promotions)

@promotions_bp.route('/<int:id>', methods=['GET'], endpoint='get_promotion')
@require_api_key
def get_promotion(id):
    promotion = get_promotion_by_id(id)
    if promotion:
        return jsonify(promotion)
    return jsonify({'error': 'Promotion not found'}), 404

@promotions_bp.route('/', methods=['POST'], endpoint='add_promotion')
@require_api_key
def add_promotion():
    data = request.get_json()
    if create_promotion(data):
        return jsonify({'message': 'Promotion created'}), 201
    return jsonify({'error': 'Failed to create promotion'}), 400

@promotions_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_promotion')
@require_api_key
def modify_promotion(id):
    data = request.get_json()
    if update_promotion(id, data):
        return jsonify({'message': 'Promotion updated'})
    return jsonify({'error': 'Failed to update promotion'}), 400

@promotions_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_promotion')
@require_api_key
def remove_promotion(id):
    if delete_promotion(id):
        return jsonify({'message': 'Promotion deleted'})
    return jsonify({'error': 'Failed to delete promotion'}), 400
