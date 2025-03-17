from db import get_connection, close_connection

def execute_query(query, params=None, fetch_one=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())

        if query.strip().lower().startswith('select'):
            if fetch_one:
                result = cursor.fetchone()

            else:
                result = cursor.fetchall()

            return result

        else:
            conn.commit()
            return cursor.rowcount

    except Exception as e:
        print(f'Error executing query: {e}')
        return None

    finally:
        cursor.close()
        close_connection(conn)

def select(table, fields="*", where=None, order_by=None, limit=None, offset=None, fetch_one=False):

    query = f"SELECT {fields} FROM {table}"

    if where:
        query += f" WHERE " + "AND ".join(f"{key} = %s"for key in where.keys())

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit:
        query += f" LIMIT {limit}"

    if offset:
        query += f" OFFSET {offset}"

    params = tuple(where.values()) if where else None
    return execute_query(query, params, fetch_one)

def insert(table, data):
    keys = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))

    query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
    params = tuple(data.values())

    return execute_query(query, params)

def update(table, data, where):
    set_clause = ', '.join(f"{key} = %s" for key in data.keys())
    where_clause = ' AND '.join(f"{key} = %s" for key in where.keys())

    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    params = tuple(data.values()) + tuple(where.values())

    return execute_query(query, params)

def delete(table, where):
    where_clause = ' AND '.join(f"{key} = %s" for key in where.keys())

    query = f"DELETE FROM {table} WHERE {where_clause}"
    params = tuple(where.values())

    return execute_query(query, params)