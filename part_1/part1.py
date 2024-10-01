import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Load the Excel file and process data
def load_data(file_path):
    return pd.read_excel(file_path, sheet_name='AXIS')  

# Generate values based on the specified parameters
def generate_values(df, update_interval, num_machines=20):
    data = []
    start_time = datetime.now()

    for machine_id in range(1, num_machines + 1):
        for _, row in df.iterrows():
            if row['FIELD NAME'] == 'axis_name':  # Skip non-numeric field
                continue

            # Determine value based on range
            value = (
                row['VALUE'] if 'CONSTANT' in row['AUTO GENERATED RANGE']
                else np.random.uniform(*map(float, row['AUTO GENERATED RANGE'].replace(' to ', ' ').split()))
            )

            timestamp = start_time + timedelta(seconds=len(data) * update_interval)
            data.append({
                'timestamp': timestamp,
                'machine_id': machine_id,
                'field': row['FIELD NAME'],
                'value': value
            })

    return pd.DataFrame(data)

# Create the database schema
def create_schema(engine):
    with engine.connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id SERIAL PRIMARY KEY,
            machine_id INT NOT NULL,
            field VARCHAR(50),
            value FLOAT,
            timestamp TIMESTAMP
        );
        """)

# Populate the database with generated data
def populate_database(engine, generated_df):
    generated_df.to_sql('machines', engine, if_exists='append', index=False)

if __name__ == "__main__":
    # Set up the database connection
    engine = create_engine('postgresql://username:siva@localhost:8000/yourdbname')

    # Define update interval in seconds
    UPDATE_INTERVAL = 0.1  # For example, every 0.1 seconds

    # Load data from the Excel file
    df = load_data('C:/Users/HW-23/Desktop/assignment/user_management/part_1/Backend Developer Task.xlsx')  # Update with your actual file path

    # Create the database schema
    create_schema(engine)

    # Generate values and populate the database
    populate_database(engine, generate_values(df, UPDATE_INTERVAL))

    print("Data generation and insertion completed successfully.")
