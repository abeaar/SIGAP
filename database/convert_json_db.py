import sqlite3
import json

# Load JSON data from files
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return []

# Load data from JSON files
tribun_data = load_json('tribun.json')
tribun_detail_data = load_json('tribun_detail.json')
hasil_analisis_data = load_json('hasil_analisis.json')

# Combine the data from all JSON files based on specific keys
data = []

# Create dictionaries for quick lookups
tribun_detail_dict = {item.get('url'): item for item in tribun_detail_data}
hasil_analisis_dict = {item.get('content'): item for item in hasil_analisis_data}

# Merge data
for tribun_item in tribun_data:
    url = tribun_item.get('url')
    merged_item = tribun_item.copy()

    # Merge with tribun_detail_data
    if url in tribun_detail_dict:
        merged_item.update(tribun_detail_dict[url])

    # Merge with hasil_analisis_data
    content = merged_item.get('content')
    if content in hasil_analisis_dict:
        merged_item.update(hasil_analisis_dict[content])

    data.append(merged_item)

# Output the combined data to a JSON file
try:
    with open('testing.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)
    print("Combined data successfully written to testing.json.")
except IOError:
    print("Error: Failed to write to testing.json.")

# Create or connect to an SQLite database
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

# Create the table
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tribun (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            content TEXT NOT NULL,
            title TEXT,
            description TEXT,
            source TEXT,
            source_url TEXT,
            time_published TEXT,
            image_url TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    print("Table 'tribun' created successfully.")
except sqlite3.Error as e:
    print(f"Error: {e}")

# Insert data into the database
try:
    for record in data:
        cursor.execute('''
            INSERT INTO tribun (url, content, title, description, source, source_url, time_published, image_url, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.get('url'),
            record.get('content'),
            record.get('title'),
            record.get('description'),
            record.get('source'),
            record.get('source_url'),
            record.get('time_published'),
            record.get('image_url'),
            record.get('category')
        ))
    conn.commit()
    print("Data successfully inserted into the SQL database.")
except sqlite3.Error as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()
