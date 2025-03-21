from query_builder import select, insert, update, delete

TABLE_NAME = 'VISITORS'

#Get all visitors
def get_all_visitors(page=1, page_size=50, sort_by="full_name", order="ASC"):
    offset = (page - 1) * page_size

    return (
        select(TABLE_NAME)
        .order_by(sort_by, order)
        .offset(offset)
        .limit(page_size)
        .execute()
    )

def get_visitor_by_id(visitor_id):
    return (
        select(TABLE_NAME)
        .where("visitor_id = %s", [visitor_id])
        .execute(fetch_one=True)
    )

def create_visitor(data):
    if not validate_visitor(data):
        raise ValueError("Invalid data for the Visitor")

    result = insert(TABLE_NAME, data)

    return result > 0

def update_visitor(visitor_id, data):
    if not validate_visitor(data):
        raise ValueError("Invalid data for the Visitor")

    result = update(TABLE_NAME, data, {'visitor_id': visitor_id})

    return result > 0

def delete_visitor(visitor_id):
    result = delete(TABLE_NAME, {'visitor_id': visitor_id})
    return result > 0

def validate_visitor(data):

    if not data.get('full_name'):
        return False

    if '@' not in data['email']:
        return False

    if len(data.get('phone', '')) < 8:
        return False

    return True