from query_builder import select, insert, update, delete

TABLE_NAME = 'ROLES'

def get_all_roles():
    return select(TABLE_NAME)

def get_role_by_id(role_id):
    return (
        select(TABLE_NAME)
        .where("role_id = %s", [role_id])
        .execute(fetch_one=True)
    )

def create_role(data):
    result = insert(TABLE_NAME, data)
    return result > 0

def update_role(role_id, data):
    result = update(TABLE_NAME, data, {'role_id': role_id})
    return result > 0

def delete_role(role_id):
    result = delete(TABLE_NAME, {'role_id': role_id})
    return result > 0
