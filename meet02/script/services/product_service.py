from query_builder import select, insert, update, delete

TABLE_NAME = 'PRODUCTS'

def get_all_products(page=1, page_size=50, sort_by="name", order="ASC", filters=None):

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

def get_product_by_id(product_id):
    return (
        select(TABLE_NAME)
        .where("product_id = %s", [product_id])
        .execute(fetch_one=True)
    )

def create_product(data):
    if not validate_product(data):
        raise ValueError("Invalid data for product")

    result = insert(TABLE_NAME, data)
    return result > 0

def update_product(product_id, data):
    if not validate_product(data):
        raise ValueError("Invalid data for product")

    result = update(TABLE_NAME, data, {'product_id': product_id})
    return result > 0

def delete_product(product_id):
    result = delete(TABLE_NAME, {'product_id': product_id})
    return result > 0

def validate_product(data):
    if data.get('price') is None or float(data.get('price')) <= 0:
        return False
    return True
