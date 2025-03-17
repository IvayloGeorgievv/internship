from query_builder import select, insert, update, delete

TABLE_NAME = 'TRANSACTIONS'

def get_all_transactions():
    return select(TABLE_NAME)

def get_transaction_by_id(transaction_id):
    return select(TABLE_NAME, where={'transaction_id': transaction_id}, fetch_one=True)

def create_transaction(data):
    result = insert(TABLE_NAME, data)
    return result > 0

def update_transaction(transaction_id, data):
    result = update(TABLE_NAME, data, {'transaction_id': transaction_id})
    return result > 0

def delete_transaction(transaction_id):
    result = delete(TABLE_NAME, {'transaction_id': transaction_id})
    return result > 0
