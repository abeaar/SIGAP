# convert_json_db.py

import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

def run():
    directory = './database'
    os.makedirs(directory, exist_ok=True)

    Base = declarative_base()
    engine = create_engine('sqlite:///database/news.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def create_model_class(tablename):
        class_name = 'Tbl_' + tablename.title().replace('_', '')
        return type(
            class_name,
            (Base,),
            {
                '__tablename__': tablename,
                '__table_args__': {'extend_existing': True},
                'id': Column(Integer, primary_key=True, autoincrement=True),
                'title': Column(String, nullable=True),
                'url': Column(String, nullable=True),
                'image': Column(String, nullable=True),
                'time_published': Column(String, nullable=True),
                'scrape_time': Column(String, nullable=True),
                'content': Column(Text, nullable=True),
                'solution': Column(Text, nullable=True),
                'category': Column(String, nullable=True),
            }
        )

    models = {}

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            tablename = os.path.splitext(filename)[0].lower()
            model = create_model_class(tablename)
            models[tablename] = model

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

            for item in data:
                news_entry = model(
                    title=item.get('title'),
                    url=item.get('url'),
                    image=item.get('image'),
                    time_published=item.get('time_published'),
                    scrape_time=item.get('scrape_time'),
                    content=item.get('content'),
                    solution=item.get('solution'),
                    category=item.get('category')
                )
                session.add(news_entry)

    Base.metadata.create_all(engine)
    session.commit()
    print("Data berhasil dimasukkan ke tabel sesuai nama file JSON.")

# Agar tetap bisa dijalankan langsung (opsional)
if __name__ == "__main__":
    run()
