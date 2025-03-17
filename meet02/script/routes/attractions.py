from flask import Blueprint, request, jsonify
from services.attraction_service import (
    get_all_attractions,
    get_attraction_by_id,
    create_attraction,
    update_attraction,
    delete_attraction
)
from utils.auth import require_api_key

attractions_bp = Blueprint('attractions', __name__)

@attractions_bp.route('/', methods=['GET'], endpoint='get_attractions')
@require_api_key
def get_attractions():
    attractions = get_all_attractions()
    return jsonify(attractions)

@attractions_bp.route('/<int:id>', methods=['GET'], endpoint='get_attraction')
@require_api_key
def get_attraction(id):
    attraction = get_attraction_by_id(id)
    if attraction:
        return jsonify(attraction)
    return jsonify({'error': 'Attraction not found'}), 404

@attractions_bp.route('/', methods=['POST'], endpoint='add_attraction')
@require_api_key
def add_attraction():
    data = request.get_json()
    if create_attraction(data):
        return jsonify({'message': 'Attraction created'}), 201
    return jsonify({'error': 'Failed to create attraction'}), 400

@attractions_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_attraction')
@require_api_key
def modify_attraction(id):
    data = request.get_json()
    if update_attraction(id, data):
        return jsonify({'message': 'Attraction updated'})
    return jsonify({'error': 'Failed to update attraction'}), 400

@attractions_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_attraction')
@require_api_key
def remove_attraction(id):
    if delete_attraction(id):
        return jsonify({'message': 'Attraction deleted'})
    return jsonify({'error': 'Failed to delete attraction'}), 400
