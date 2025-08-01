📂 Struktur Endpoint API
🔹 1. Berita Terkini
GET /terkini
Mengambil seluruh berita terbaru dari berbagai portal.

Contoh:

bash
Copy
Edit
GET /terkini
GET /terkini?include_all=true
Query Parameters:

include_all (optional): jika true, akan menampilkan seluruh data (bukan hanya 100 terakhir).

🔹 2. Berita Terpopuler
GET /terpopuler
Mengambil seluruh berita populer dari berbagai portal.

Contoh:

bash
Copy
Edit
GET /terpopuler
GET /terpopuler?include_all=true
🔹 3. Berita per Portal
GET /news/{portal}
Menampilkan berita dari satu portal tertentu (misal: kompas, cnn, detik, dll).

Contoh:

bash
Copy
Edit
GET /news/kompas
🔹 4. Berita per Kategori
GET /category/{kategori}
Menampilkan berita dari semua portal berdasarkan kategori yang diprediksi (oleh LLama 3.2).

Kategori yang tersedia: politik, ekonomi, kriminal, olahraga, hiburan, kesehatan, teknologi, dll.

Contoh:

bash
Copy
Edit
GET /category/politik
🔹 5. Berita per Portal & Kategori
GET /news/category/{portal}/{kategori}
Gabungan filter berdasarkan portal dan kategori.

Contoh:

swift
Copy
Edit
GET /news/category/cnn/ekonomi
🗃️ Penyimpanan Database
Semua data disimpan dalam database SQLite, dipisah berdasarkan jenis:

terkini_kompas, terpopuler_kompas

terkini_cnn, terpopuler_cnn

terkini_detik, terpopuler_detik

🔄 Jadwal Scraping Otomatis
Scraping dan analisis dijalankan otomatis setiap hari pukul 03:00 WIB melalui task async.

🧠 Analisis dan Klasifikasi
Model LLama 3.2 digunakan untuk:

Meringkas isi berita

Memprediksi kategori berita

🛠️ Teknologi yang Digunakan
FastAPI

SQLite

Python 3.10+

Uvicorn

LLama 3.2 (text summarization & classification)

Cron/asyncio untuk penjadwalan scraping
