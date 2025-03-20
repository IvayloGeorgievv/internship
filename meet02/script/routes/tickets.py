from flask import Blueprint, request, jsonify
from services.ticket_service import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket,
    delete_ticket,
)
from utils.auth import require_api_key

tickets_bp = Blueprint('tickets', __name__)

#Get all tickets
@tickets_bp.route('/', methods=['GET'], endpoint='get_tickets')
@require_api_key
def get_tickets():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    sort_by = request.args.get('sort_by', 'purchase_date', type=str)
    order = request.args.get('order', 'DESC', type=str)

    filters = {}
    for key in request.args:
        if key not in ['page', 'page_size', 'sort_by', 'order']:
            filters[key] = request.args.getlist(key)

    tickets = get_all_tickets(page, page_size, sort_by, order, filters)
    return jsonify(tickets)

#Get Ticket by id
@tickets_bp.route('/<int:id>', methods=['GET'], endpoint='get_ticket')
@require_api_key
def get_ticket(id):
    ticket = get_ticket_by_id(id)
    if ticket:
        return jsonify(ticket)
    return jsonify({'error': 'Ticket not found'}), 404

#Add ticket
@tickets_bp.route('/', methods=['POST'], endpoint='add_ticket')
@require_api_key
def add_ticket():
    data = request.get_json()
    if create_ticket(data):
        return jsonify({'message': 'Ticket created'}), 201
    return jsonify({'error': 'Failed to create ticket'}), 400

#Update ticket
@tickets_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_ticket')
@require_api_key
def modify_ticket(id):
    data = request.get_json()
    if update_ticket(id, data):
        return jsonify({'message': 'Ticket updated'})
    return jsonify({'error': 'Failed to update ticket'}), 400

#Delete ticket
@tickets_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_ticket')
@require_api_key
def remove_ticket(id):
    if delete_ticket(id):
        return jsonify({'message': 'Ticket deleted'})
    return jsonify({'error': 'Failed to delete ticket'}), 400
