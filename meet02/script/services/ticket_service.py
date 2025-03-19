from query_builder import select, insert, update, delete

TABLE_NAME = 'TICKETS'

def get_all_tickets(page=1, page_size=50, sort_by="purchase_date", order="DESC"):

    offset = (page - 1) * page_size

    return (
        select(TABLE_NAME)
        .order_by(sort_by, order)
        .offset(offset)
        .limit(page_size)
        .execute()
    )

def get_ticket_by_id(ticket_id):
    return (
        select(TABLE_NAME)
        .where("ticket_id = %s", [ticket_id])
        .execute(fetch_one=True)
    )

def create_ticket(data):
    if not validate_ticket(data):
        raise ValueError("Invalid data for ticket")

    result = insert(TABLE_NAME, data)

    return result > 0

def update_ticket(ticket_id, data):
    if not validate_ticket(data):
        raise ValueError("Invalid data for ticket")

    result = update(TABLE_NAME, data, {'ticket_id': ticket_id})

    return result > 0

def delete_ticket(ticket_id):

    result = delete(TABLE_NAME, {'ticket_id': ticket_id})

    return result > 0

def validate_ticket(data):

    valid_ticket_types = ['General', 'VIP', 'Season Pass', 'Student', 'Senior']

    if data.get('ticket_type') not in valid_ticket_types:
        return False

    valid_statuses = ['Active', 'Used', 'Expired']
    if data.get('status') not in valid_statuses:
        return False

    if data.get('price') is None or float(data.get('price')) <= 0:
        return False

    return True
