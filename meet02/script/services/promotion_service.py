from query_builder import select, insert, update, delete

TABLE_NAME = 'PROMOTIONS'

def get_all_promotions(page=1, page_size=50, sort_by="start_date", order="ASC"):
    offset = (page - 1) * page_size
    return (
        select(TABLE_NAME)
        .order_by(sort_by, order)
        .limit(page_size)
        .offset(offset)
        .execute()
    )

def get_promotion_by_id(promotion_id):
    return (
        select(TABLE_NAME)
        .where("promotion_id = %s", [promotion_id])
        .execute(fetch_one=True)
    )

def create_promotion(data):
    result = insert(TABLE_NAME, data)
    return result > 0

def update_promotion(promotion_id, data):
    result = update(TABLE_NAME, data, {'promotion_id': promotion_id})
    return result > 0

def delete_promotion(promotion_id):
    result = delete(TABLE_NAME, {'promotion_id': promotion_id})
    return result > 0
