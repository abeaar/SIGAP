from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Setup database connection
DATABASE_URL = "sqlite:///news.db"  # URL untuk SQLite database

# Step 2: Setup base class for models
Base = declarative_base()

# Step 3: Define the model (table) for SQLAlchemy
class News(Base):
    __tablename__ = 'TRIBUN'  # Nama tabel yang ada di database

    ID = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(Integer)
    description= Column(String)
    source= Column(String)
    source_url= Column(String)
    time_published= Column(String)
    image_url= Column(String)

# Step 4: Create engine and session
engine = create_engine(DATABASE_URL, echo=True)  # echo=True untuk melihat query yang dijalankan
Session = sessionmaker(bind=engine)
session = Session()

# Step 5: Create the table in the database if it doesn't exist
Base.metadata.create_all(engine)

# Step 7: Menampilkan semua data dari tabel
def get_all_people():
    people = session.query(News).all()
    for news_item in people:
        print(f"ID: {news_item.ID}, Title: {news_item.title}, URL: {news_item.url}, Description: {news_item.description}, Source: {news_item.source}, Source URL: {news_item.source_url}, Time Published: {news_item.time_published}, Image URL: {news_item.image_url}")

# Step 8: Menutup sesi
def close_session():
    session.close()

# Contoh penggunaan
if __name__ == "__main__":

    # Menampilkan data
    print("People in the database:")
    get_all_people()

    # Menutup sesi
    close_session()
