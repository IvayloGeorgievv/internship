from query_builder import select, insert, update, delete

TABLE_NAME = 'TRANSACTIONS'

def get_all_transactions(page=1, page_size=50, sort_by="transaction_date", order="DESC", filters=None):

    qb = select(TABLE_NAME).select("*")

    if filters:
        for key, values in filters.items():
            if isinstance(values, list) and len(values) > 1:
                qb.where(f"{key} = %s", [values[0]])
                for v in values[1:]:
                    qb.where(f"{key} = %s", [v])
                continue

            qb.where(f"{key} = %s", [values[0]])

    offset_value = (page - 1) * page_size
    return qb.orderBy(sort_by, order).limit(page_size).offset(offset_value).execute()

def get_transaction_by_id(transaction_id):
    return (
        select(TABLE_NAME)
        .where("transaction_id = %s", [transaction_id])
        .execute(fetch_one=True)
    )

def create_transaction(data):
    result = insert(TABLE_NAME, data)
    return result > 0

def update_transaction(transaction_id, data):
    result = update(TABLE_NAME, data, {'transaction_id': transaction_id})
    return result > 0

def delete_transaction(transaction_id):
    result = delete(TABLE_NAME, {'transaction_id': transaction_id})
    return result > 0
