import sqlite3
import json

# Open the JSON file and load data
with open('tribun.json', 'r') as json_file:
    data = json.load(json_file)
    print(data)  # Print the loaded JSON data for debugging

# Create or connect to an SQLite database
conn = sqlite3.connect('news.db')  # Replace with your database name
cursor = conn.cursor()

# Create a table based on the keys of the first item in the JSON data
# Assumption: Your JSON data is a list of dictionaries (list of records)
columns = ', '.join(data[0].keys())  # Get column names
columns_with_types = ', '.join([f"{key} TEXT" for key in data[0].keys()])  # Define all columns as TEXT
create_table_query = f"CREATE TABLE IF NOT EXISTS TRIBUN (ID INTEGER PRIMARY KEY AUTOINCREMENT, {columns_with_types})"

# Execute the table creation query
cursor.execute(create_table_query)

# Insert data into the table
for record in data:
    # Add the placeholders for each value, excluding ID (ID will be auto-generated)
    placeholders = ', '.join('?' * len(record))  
    insert_query = f"INSERT INTO TRIBUN ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(record.values()))  # Insert each record

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data successfully inserted into the SQL database.")
