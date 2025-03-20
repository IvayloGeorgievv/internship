from flask import Blueprint, request, jsonify
from services.visitor_service import (
    get_all_visitors,
    get_visitor_by_id,
    create_visitor,
    update_visitor,
    delete_visitor
)
from utils.auth import require_api_key

visitors_bp = Blueprint('visitors', __name__)

#Get All Visitors
@visitors_bp.route('/', methods=['GET'], endpoint='get_visitors')
@require_api_key
# Not going to add filters to visitors because records in real world would be uniq we cannot filter them
def get_visitors():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    sort_by = request.args.get('sort_by', 'full_name', type=str)
    order = request.args.get('order', 'ASC', type=str)

    visitors = get_all_visitors(page, page_size, sort_by, order)
    return jsonify(visitors)

#Get Visitor by id
@visitors_bp.route('/<int:id>', methods=['GET'], endpoint='get_visitor')
@require_api_key
def get_visitor(id):
    visitor = get_visitor_by_id(id)
    if visitor:
        return jsonify(visitor)
    return jsonify({'message': 'Visitor not found'}), 404

#POST - Create new visitor
@visitors_bp.route('/', methods=['POST'], endpoint='add_visitor')
@require_api_key
def add_visitor():
    data = request.get_json()
    if create_visitor(data):
        return jsonify({'message': 'Visitor created'}), 201
    return jsonify({'message': 'Failed to create visitor'}), 400

#PUT - Update visitor
@visitors_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_visitor')
@require_api_key
def modify_visitor(id):
    data = request.get_json()
    if update_visitor(id, data):
        return jsonify({'message': 'Visitor updated'})
    return jsonify({'message': 'Failed to update visitor'}), 400

#DELETE - Delete visitor
@visitors_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_visitor')
@require_api_key
def remove_visitor(id):
    if delete_visitor(id):
        return jsonify({'message': 'Visitor deleted'})
    return jsonify({'message': 'Failed to delete visitor'}), 400
