import os
import shutil

from config import get_snowflake_connection
from data_generation import generate_all_data
from generate_csv import generate_csv
from table_config import TABLE_CONFIG


def run_script(business_climate):
    print(f"Running {business_climate} business climate script ...")

    # Generate the data
    attractions, roles, employees, establishments, products, promotions, visitors, tickets, sales, transactions = generate_all_data(business_climate)

    # Generate csv files
    generate_all_csv_files(attractions, roles, employees, establishments, products, promotions, visitors, tickets, sales, transactions)

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:

        #Upload cvs files into Snowflake
        import_csv_files(cursor)

        #Load the data from csv into transient tables
        load_into_transient_tables(cursor)

        #Load VALID data from transient to actual tables
        transfer_valid_data(cursor)

        clean_transient_tables(cursor)

        #Remove the csv files from Snowflake
        delete_csv_files(cursor)

        delete_data_folder()


    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def generate_all_csv_files(attractions, roles, employees, establishments, products, promotions, visitors, tickets, sales, transactions):

    csv_data = {
        'visitors.csv': visitors,
        'tickets.csv': tickets,
        'attractions.csv': attractions,
        'establishments.csv': establishments,
        'roles.csv': roles,
        'employees.csv': employees,
        'products.csv': products,
        'promotions.csv': promotions,
        'sales.csv': sales,
        'transactions.csv': transactions
    }

    for filename, data in csv_data.items():
        if data:
            generate_csv(filename, data)
        else:
            print(f"Skipping {filename} - There is no data for it")



# Func to separate the import csv logic
def import_csv_files(cursor):
    try:
        print("Importing CSV files into Snowflake...")

        files = ['visitors.csv', 'tickets.csv', 'attractions.csv', 'roles.csv',
                 'employees.csv', 'products.csv', 'promotions.csv', 'sales.csv', 'transactions.csv', 'establishments.csv']

        for file in files:
            file_path = os.path.join('data', file)

            cursor.execute(f"PUT file://{file_path} @my_stage")

    except Exception as e:
        print(f"Error during importing file upload: {e}")
        raise


def load_into_transient_tables(cursor):
    try:
        print("Loading data into transient tables...")

        cursor.execute("""USE DATABASE MEET_ONE""")

        for table, config in TABLE_CONFIG.items():

            # If there is a Transient table for this entity use it to load the csv data there and if there is not -
            # Use the actual table
            load_table = config['stage_table'] if config['stage_table'] else table
            columns = config['transient_columns'] if config['transient_columns'] else config['columns']

            file = config['file']
            query = f"""
                    COPY INTO {load_table} ({columns})
                    FROM @my_stage/{file}
                    FILE_FORMAT = (FORMAT_NAME = 'my_csv_format')
                    ;           
                    """
            cursor.execute(query)

    except Exception as e:
        print(f"Error loading data into transient tables: {e}")
        raise


def transfer_valid_data(cursor):
    try:
        print("Transferring VALID data into actual tables...")
        cursor.execute("USE DATABASE MEET_ONE")
        for table, config in TABLE_CONFIG.items():
            if not config['stage_table']:
                continue
            print(f"Transferring VALID data into {table} table...")
            cols = config['columns']
            sel_cols = config.get('transfer_columns', config['transient_columns'])
            query = f"""
                INSERT INTO {table} ({cols})
                SELECT {sel_cols}
                FROM {config['stage_table']}
                {config['joins']}
                WHERE {config['conditions']};
            """
            cursor.execute(query)
    except Exception as e:
        print(f"Error transferring data into actual tables: {e}")
        raise


def clean_transient_tables(cursor):

    print("Cleaning transient tables from VALID data...")

    for table, config in TABLE_CONFIG.items():

        if not config['stage_table'] or not config['conditions']:
            continue

        query = f"""
                DELETE FROM {config['stage_table']}
                WHERE {config['conditions']};
                """

        cursor.execute(query)

def delete_csv_files(cursor):
    try:
        print("Deleting CSV files from Snowflake...")

        files = [config['file'] for config in TABLE_CONFIG.values() if config['file']]

        for file in files:
            query = f"REMOVE @my_stage/{file};"
            cursor.execute(query)

        print("All CSV files deleted from Snowflake")

    except Exception as e:
        print(f"Error during CSV file deletion: {e}")
        raise

#Deleting data folder where generated csv files are
def delete_data_folder(directory='data'):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Deleted folder: {directory}")
    else:
        print(f"Folder '{directory}' does not exist.")