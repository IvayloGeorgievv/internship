import snowflake.connector
from config import SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA

def get_connection():
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        print("Snowflake connection established!")
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        raise

def close_connection(conn):
    try:
        if conn:
            conn.close()
            print("Snowflake connection closed!")
    except Exception as e:
        print(f"Error closing Snowflake connection: {e}")
