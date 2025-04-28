import sqlite3
import json

# Open the JSON files and load data
with open('tribun.json', 'r', encoding='utf-8') as json_file:
    tribun_data = json.load(json_file)

with open('tribun_detail.json', 'r', encoding='utf-8') as json_file:
    tribun_detail_data = json.load(json_file)

with open('hasil_analisis.json', 'r', encoding='utf-8') as json_file:
    hasil_analisis_data = json.load(json_file)

# Combine the data from all JSON files based on specific keys
data = []

# Create a dictionary for quick lookup of tribun_detail_data by 'url'
tribun_detail_dict = {item['url']: item for item in tribun_detail_data}

# Create a dictionary for quick lookup of hasil_analisis_data by 'content'
hasil_analisis_dict = {item['content']: item for item in hasil_analisis_data}

# Merge tribun_data with tribun_detail_data based on 'url'
for tribun_item in tribun_data:
    url = tribun_item.get('url')
    merged_item = tribun_item.copy()
    
    if url in tribun_detail_dict:
        merged_item.update(tribun_detail_dict[url])
    
    # Merge with hasil_analisis_data based on 'content'
    content = merged_item.get('content')
    if content in hasil_analisis_dict:
        merged_item.update(hasil_analisis_dict[content])
    
    data.append(merged_item)

# Output the combined data to a JSON file
with open('testing.json', 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

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
