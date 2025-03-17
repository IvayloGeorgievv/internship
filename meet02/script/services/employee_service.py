from query_builder import select, insert, update, delete

TABLE_NAME = 'EMPLOYEES'


def get_all_employees(page=1, page_size=50, sort_by="full_name", order="ASC"):
    offset = (page - 1) * page_size
    order_by = f"{sort_by} {order}"

    return select(
        TABLE_NAME,
        order_by=order_by,
        limit=page_size,
        offset=offset
    )


def get_employee_by_id(employee_id):
    return select(
        TABLE_NAME,
        where={'employee_id': employee_id},
        fetch_one=True
    )


def create_employee(data):
    if not validate_employee(data):
        raise ValueError("Invalid data for employee")

    result = insert(TABLE_NAME, data)
    return result > 0


def update_employee(employee_id, data):
    if not validate_employee(data):
        raise ValueError("Invalid data for employee")

    result = update(TABLE_NAME, data, {'employee_id': employee_id})
    return result > 0


def delete_employee(employee_id):
    result = delete(TABLE_NAME, {'employee_id': employee_id})
    return result > 0


def validate_employee(data):
    if not data.get('full_name'):
        return False

    if data.get('salary') is None or float(data.get('salary')) <= 0:
        return False

    valid_statuses = ['Active', 'On Leave', 'Resigned']
    if data.get('status') not in valid_statuses:
        return False

    return True
