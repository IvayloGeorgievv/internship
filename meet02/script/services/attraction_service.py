from query_builder import select, insert, update, delete

TABLE_NAME = 'ATTRACTIONS'

def get_all_attractions(page=1, page_size=50, sort_by="name", order="DESC"):

    offset = (page - 1) * page_size
    order_by = f"{sort_by} {order}"

    return select(
        TABLE_NAME,
        order_by=order_by,
        limit=page_size,
        offset=offset,
    )

def get_attraction_by_id(attr_id):
    return select(
        TABLE_NAME,
        where={'attraction_id': attr_id},
        fetch_one=True
    )

def create_attraction(data):
    if not validate_attraction(data):
        raise ValueError("Invalid data for attraction")

    result = insert(TABLE_NAME, data)
    return result > 0

def update_attraction(attr_id, data):
    if not validate_attraction(data):
        raise ValueError("Invalid data for attraction")

    result = update(TABLE_NAME,data, {'attraction_id': attr_id})
    return result > 0

def delete_attraction(attr_id):

    result = delete(TABLE_NAME, {'attraction_id': attr_id})
    return result > 0

def validate_attraction(data):

    valid_statuses = ['Operational', 'Closed', 'Maintenance']
    if data.get('status') not in valid_statuses:
        return False

    if data.get('capacity') <= 0:
        return False

    return True