import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user=os.environ.get("SNOWFLAKE_USER"),
            password=os.environ.get("SNOWFLAKE_PASSWORD"),
            account=os.environ.get("SNOWFLAKE_ACCOUNT"),
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SNOWFLAKE_DATABASE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA"),
            session_parameters={
                'QUERY_RESULT_FORMAT': 'JSON'
            }
        )
        print("Connection established")
        return conn

    except snowflake.connector.errors.DatabaseError as db_err:
        print(f"Database Error: {db_err}")
        raise
    except Exception as e:
        print(f"General Error connecting to Snowflake: {e}")
        raise