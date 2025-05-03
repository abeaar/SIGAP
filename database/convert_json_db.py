import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Directory containing JSON files
directory = 'e:\\Program\\KP\\backend\\database'

# List to store combined data
combined_data = []

# Iterate through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
                if isinstance(data, list):  # Ensure the JSON file contains a list of records
                    combined_data.extend(data)
                else:
                    print(f"Skipping {filename}: Not a list of records.")
            except json.JSONDecodeError as e:
                print(f"Error decoding {filename}: {e}")

# Ensure there is data to process
if not combined_data:
    print("No valid JSON data found.")
else:
    # Write combined data to a new JSON file
    output_file = os.path.join(directory, 'combined_news.json')
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    print(f"Combined JSON data has been written to {output_file}")

json_file_path = output_file
# Database connection and setup

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine('sqlite:///news.db')  # SQLite database file
Session = sessionmaker(bind=engine)
session = Session()

# Define the News model
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    image = Column(String, nullable=True)
    category = Column(String, nullable=True)
    datetime = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)

# Create the table
Base.metadata.create_all(engine)

# Read the combined JSON file
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Insert data into the database
    for item in data:
        news_entry = News(
            title=item.get('title'),
            url=item.get('url'),
            image=item.get('image'),
            category=item.get('category'),
            datetime=item.get('datetime'),
            content=item.get('content'),
            solution=item.get('solution')
        )
        session.add(news_entry)

    # Commit the transaction
    session.commit()
    print("Data successfully inserted into the database.")
else:
    print(f"File {json_file_path} not found.")