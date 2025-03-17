from flask import Blueprint, request, jsonify
from services.transaction_service import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction
)
from utils.auth import require_api_key

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'], endpoint='get_transactions')
@require_api_key
def get_transactions():
    transactions = get_all_transactions()
    return jsonify(transactions)

@transactions_bp.route('/<int:id>', methods=['GET'], endpoint='get_transaction')
@require_api_key
def get_transaction(id):
    transaction = get_transaction_by_id(id)
    if transaction:
        return jsonify(transaction)
    return jsonify({'error': 'Transaction not found'}), 404

@transactions_bp.route('/', methods=['POST'], endpoint='add_transaction')
@require_api_key
def add_transaction():
    data = request.get_json()
    if create_transaction(data):
        return jsonify({'message': 'Transaction created'}), 201
    return jsonify({'error': 'Failed to create transaction'}), 400

@transactions_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_transaction')
@require_api_key
def modify_transaction(id):
    data = request.get_json()
    if update_transaction(id, data):
        return jsonify({'message': 'Transaction updated'})
    return jsonify({'error': 'Failed to update transaction'}), 400

@transactions_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_transaction')
@require_api_key
def remove_transaction(id):
    if delete_transaction(id):
        return jsonify({'message': 'Transaction deleted'})
    return jsonify({'error': 'Failed to remove transaction'}), 400
