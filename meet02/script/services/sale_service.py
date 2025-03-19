from query_builder import select, insert, update, delete

TABLE_NAME = 'SALES'

def get_all_sales(page=1, page_size=50, sort_by="sale_date", order="DESC"):
    offset = (page - 1) * page_size

    return (
        select(TABLE_NAME)
        .order_by(sort_by, order)
        .limit(page_size)
        .offset(offset)
        .execute()
    )

def get_sale_by_id(sale_id):
    return (
        select(TABLE_NAME)
        .where("sale_id = %s", [sale_id])
        .execute(fetch_one=True)
    )

def create_sale(data):
    # First, insert into SALES table
    sale_result = insert(TABLE_NAME, data)
    if sale_result > 0:
        sale = get_sale_by_id(sale_result)
        if sale:
            create_transaction_for_sale(sale)
            return True

    return False


def create_transaction_for_sale(sale):
    transaction_data = {
        'sale_id': sale['sale_id'],
        'employee_id': sale.get('employee_id'),
        'visitor_id': sale.get('visitor_id'),
        'amount': sale['total_price'],
        'transaction_type': 'Product Sale',
    }

    # Insert into transaction table
    insert("TRANSACTIONS", transaction_data)


def update_sale(sale_id, data):
    result = update(TABLE_NAME, data, {'sale_id': sale_id})
    return result > 0

def delete_sale(sale_id):
    result = delete(TABLE_NAME, {'sale_id': sale_id})
    return result > 0
