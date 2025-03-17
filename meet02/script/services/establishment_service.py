from query_builder import select, insert, update, delete

TABLE_NAME = 'ESTABLISHMENTS'

def get_all_establishments(page=1, page_size=50, sort_by="name", order="ASC"):
    offset = (page - 1) * page_size
    order_by = f"{sort_by} {order}"

    return select(TABLE_NAME, order_by=order_by, limit=page_size, offset=offset)

def get_establishment_by_id(establishment_id):
    return select(TABLE_NAME, where={'establishment_id': establishment_id}, fetch_one=True)

def create_establishment(data):
    if not validate_establishment(data):
        raise ValueError("Invalid data for establishment")

    result = insert(TABLE_NAME, data)
    return result > 0

def update_establishment(establishment_id, data):
    if not validate_establishment(data):
        raise ValueError("Invalid data for establishment")

    result = update(TABLE_NAME, data, {'establishment_id': establishment_id})
    return result > 0

def delete_establishment(establishment_id):
    result = delete(TABLE_NAME, {'establishment_id': establishment_id})
    return result > 0

def validate_establishment(data):
    valid_categories = ['Restaurant', 'Shop']
    if data.get('category') not in valid_categories:
        return False
    return True
