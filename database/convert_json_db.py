import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

directory = 'C:/Programming/Kuliah/SIGAP/database'

Base = declarative_base()
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

# Fungsi untuk membuat model dinamis sesuai nama tabel
def create_model_class(tablename):
    class_name = ''.join(word.capitalize() for word in tablename.split('_'))
    return type(
        class_name,
        (Base,),
        {
            '__tablename__': tablename,
            'id': Column(Integer, primary_key=True, autoincrement=True),
            'title': Column(String, nullable=True),
            'url': Column(String, nullable=True),
            'image': Column(String, nullable=True),
            'category': Column(String, nullable=True),
            'datetime': Column(String, nullable=True),
            'content': Column(Text, nullable=True),
            'solution': Column(Text, nullable=True),
        }
    )

models = {}  # dictionary untuk simpan model berdasarkan nama tabel

# Iterasi file JSON, buat model untuk setiap file JSON
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        tablename = os.path.splitext(filename)[0].lower()  # ambil nama file tanpa ekstensi
        model = create_model_class(tablename)
        models[tablename] = model

# Buat semua tabel dulu
Base.metadata.create_all(engine)

# Read tiap file dan insert ke tabel masing-masing
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        tablename = os.path.splitext(filename)[0].lower()
        model = models[tablename]

        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"{filename} tidak berisi list, dilewati.")
                    continue
            except json.JSONDecodeError as e:
                print(f"Error decode {filename}: {e}")
                continue

        # Insert data ke tabel sesuai model
        for item in data:
            news_entry = model(
                title=item.get('title'),
                url=item.get('url'),
                image=item.get('image'),
                category=item.get('category'),
                datetime=item.get('datetime'),
                content=item.get('content'),
                solution=item.get('solution')
            )
            session.add(news_entry)

# Commit semua insert
session.commit()
print("Data berhasil dimasukkan ke tabel sesuai nama file JSON.")
