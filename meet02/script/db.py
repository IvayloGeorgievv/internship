import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

class SnowflakeConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(SnowflakeConnection, cls).__new__(cls)
                cls._instance.conn = snowflake.connector.connect(
                    user = os.getenv('SNOWFLAKE_USER'),
                    password = os.getenv('SNOWFLAKE_PASSWORD'),
                    account = os.getenv('SNOWFLAKE_ACCOUNT'),
                    database = os.getenv('SNOWFLAKE_DATABASE'),
                    schema = os.getenv('SNOWFLAKE_SCHEMA')
                )
                print("Snowflake connection established")
            except Exception as e:
                print(f"Error connecting to Snowflake: {e}")
                raise
        return cls._instance

    def get_connection(self):
        return self.conn

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
                print("Snowflake connection closed")
        except Exception as e:
            print(f"Error closing Snowflake connection: {e}")


def get_connection():
    return SnowflakeConnection().get_connection()

