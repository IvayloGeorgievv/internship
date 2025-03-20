from query_builder import select, insert, update, delete

TABLE_NAME = 'ATTRACTIONS'

def get_all_attractions(page=1, page_size=50, sort_by="name", order="DESC", filters=None):

    # Storing select part in qb variable so we can add filtering logic by concatenating to the variable
    qb = select(TABLE_NAME).select("*")

    if filters:
        for key, values in filters.items():
           # Checking if we have more than 1 filter to filter by and if we have more than one value for an attribute
           # example -> ?status=Operational&status=Maintenance
            if isinstance(values, list) and len(values) > 1:
                qb.where(f"{key} = %s", [values[0]])
                for v in values[1:]:
                    qb.orWhere(f"{key} = %s", [v])
                # Using continue to skip the logic for having only 1 filter
                continue

            qb.where(f"{key} = %s", [values[0]])

    offset_value = (page - 1) * page_size
    return qb.orderBy(sort_by, order).limit(page_size).offset(offset_value).execute()

def get_attraction_by_id(attr_id):
    return (
        select(TABLE_NAME)
        .where("attraction_id = %s", [attr_id])
        .execute(fetch_one=True)
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