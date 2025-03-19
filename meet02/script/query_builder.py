from db import get_connection

class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.query = ""
        self.params = []


    def select(self, fields):
        self.query = f"SELECT {fields} FROM {self.table}"
        return self

    def where(self, condition, params=None):
        if "WHERE" in self.query:
            return self.andWhere(condition, params)

        self.query += f" WHERE {condition}"

        if params:
            for param in params:
                self.params.append(param)

        return self

    def andWhere(self, condition, params=None):
        self.query += f" AND {condition}"
        if params:
            for param in params:
                self.params.append(param)

        return self


    def orWhere(self, condition, params=None):
        self.query += f" OR {condition}"

        if params:
            for param in params:
                self.params.append(params)

        return self

    def orderBy(self, field, direction="ASC"):
        self.query += f" ORDER BY {field} {direction}"

        return self

    def limit(self, limit):
        self.query += f" LIMIT %s"
        self.params.append(limit)

        return self

    def offset(self, offset):
        self.query += f" OFFSET %s"
        self.params.append(offset)

        return self

    def groupBy(self, field):
        self.query += f" GROUP BY {field}"

        return self

    def execute(self, fetch_one=False):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(self.query, tuple(self.params))

            if self.query.strip().lower().startswith("select"):
                if fetch_one:
                    return cursor.fetchone()

                return cursor.fetchone()

            connection.commit()
            return cursor.rowcount

        except Exception as e:
            print(f"Error executing query: {e}")
            return None

        finally:
            cursor.close()


def select(table):
    return QueryBuilder(table)

def insert(table, data):
    keys = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))

    query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
    params = []
    for value in data.values():
        params.append(value)

    return execute_query(query, params)

def update(table, data, where):

    # Made this check so we update only based on 1 unique parameter for example the id -> WHERE id = ...
    if len(where) != 1:
        raise ValueError("Only one condition is allowed in WHERE clause for update")

    set_clause = []
    params = []
    for key in data.keys():
        set_clause.append(f"{key} = %s")
        params.append(data[key])

    key, value = list(where.items())[0] # Extracting the first and only entry from where to append the param to the list of params
    where_clause = f"{where} = %s"
    params.append(value)


    query = f"UPDATE {table} SET {', '.join(set_clause)} WHERE {where_clause}"
    return execute_query(query, params)

def delete(table, where):

    # Made this check so we delete only based on 1 unique parameter for example the id -> WHERE id = ...
    if len(where) != 1:
        raise ValueError("Only one condition is allowed in WHERE clause for update")

    params = []
    key, value = list(where.items())[0]
    where_clause = f"{where} = %s"
    params.append(value)

    query = f"DELETE FROM {table} WHERE {where_clause}"

    return execute_query(query, params)

#Used for insert, update, delete
def execute_query(query, params):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, tuple[params])
    connection.commit()

    return cursor.rowcount
