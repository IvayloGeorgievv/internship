from flask import Blueprint, request, jsonify
from services.employee_service import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)
from utils.auth import require_api_key

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'], endpoint='get_employees')
@require_api_key
def get_employees():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    sort_by = request.args.get('sort_by', 'full_name', type=str)
    order = request.args.get('order', 'ASC', type=str)

    filters = {}
    for key in request.args:
        if key not in ['page', 'page_size', 'sort_by', 'order']:
            filters[key] = request.args.getlist(key)

    employees = get_all_employees(page, page_size, sort_by, order, filters)
    return jsonify(employees)

@employees_bp.route('/<int:id>', methods=['GET'], endpoint='get_employee')
@require_api_key
def get_employee(id):
    employee = get_employee_by_id(id)
    if employee:
        return jsonify(employee)
    return jsonify({'error': 'Employee not found'}), 404

@employees_bp.route('/', methods=['POST'], endpoint='add_employee')
@require_api_key
def add_employee():
    data = request.get_json()
    if create_employee(data):
        return jsonify({'message': 'Employee created'}), 201
    return jsonify({'error': 'Failed to create employee'}), 400

@employees_bp.route('/<int:id>', methods=['PUT'], endpoint='modify_employee')
@require_api_key
def modify_employee(id):
    data = request.get_json()
    if update_employee(id, data):
        return jsonify({'message': 'Employee updated'})
    return jsonify({'error': 'Failed to update employee'}), 400

@employees_bp.route('/<int:id>', methods=['DELETE'], endpoint='remove_employee')
@require_api_key
def remove_employee(id):
    if delete_employee(id):
        return jsonify({'message': 'Employee deleted'})
    return jsonify({'error': 'Failed to delete employee'}), 400
