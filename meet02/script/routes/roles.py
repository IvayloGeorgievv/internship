from flask import Blueprint, request, jsonify
from services.role_service import (
    get_all_roles,
    get_role_by_id,
    create_role,
    update_role,
    delete_role
)
from utils.auth import require_api_key

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/', methods=['GET'], endpoint='get_roles')
@require_api_key
# Not adding filters to roles because at the moment there are 5 roles
def get_roles():
    roles = get_all_roles()
    return jsonify(roles)

@roles_bp.route('/<int:id>', methods=['GET'], endpoint='get_role')
@require_api_key
def get_role(id):
    role = get_role_by_id(id)
    if role:
        return jsonify(role)
    return jsonify({'error': 'Role not found'}), 404

@roles_bp.route('/', methods=['POST'], endpoint='add_role')
@require_api_key
def add_role():
    data = request.get_json()
    if create_role(data):
        return jsonify({'message': 'Role created'}), 201
    return jsonify({'error': 'Failed to create role'}), 400

@roles_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_role')
@require_api_key
def modify_role(id):
    data = request.get_json()
    if update_role(id, data):
        return jsonify({'message': 'Role updated'})
    return jsonify({'error': 'Failed to update role'}), 400

@roles_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_role')
@require_api_key
def remove_role(id):
    if delete_role(id):
        return jsonify({'message': 'Role deleted'})
    return jsonify({'error': 'Failed to delete role'}), 400
