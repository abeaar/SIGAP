# 📰 FastAPI News Scraper API

Sebuah API backend yang dibangun menggunakan [FastAPI](https://fastapi.tiangolo.com/) untuk menyediakan berbagai jenis berita hasil scraping dari berbagai portal berita Indonesia.

## 🚀 Fitur Utama

- Menyediakan berita terbaru dan terpopuler.
- Mendukung filter berdasarkan portal atau kategori.
- Performa tinggi dengan FastAPI dan struktur modular.

## 📌 Dokumentasi API

### `GET /terkini`

Menyediakan berita terbaru berdasarkan waktu scraping terakhir.

**Query Parameters:**
- `include_all=true` _(opsional)_: Jika diaktifkan, menampilkan seluruh data tanpa batasan jumlah.

**Contoh:**
GET /terkini
GET /terkini?include_all=true

yaml
Copy
Edit

---

### `GET /terpopuler`

Menyediakan daftar berita populer dari berbagai portal.

**Contoh:**
GET /terpopuler

yaml
Copy
Edit

---

### `GET /news/{portal}`

Menampilkan semua berita dari satu portal tertentu.

**Parameter:**
- `{portal}`: Nama portal berita, misalnya: `kompas`, `cnn`, `detik`, dll.

**Contoh:**
GET /news/kompas

yaml
Copy
Edit

---

### `GET /category/{category}`

Menampilkan berita berdasarkan kategori tertentu.

**Parameter:**
- `{category}`: Nama kategori, misalnya: `politik`, `ekonomi`, `kriminal`, dll.

**Contoh:**
GET /category/ekonomi

yaml
Copy
Edit

---

### `GET /news/category/{portal}/{category}`

Menampilkan berita dari satu portal dan kategori tertentu.

**Parameter:**
- `{portal}`: Nama portal berita, misalnya `kompas`
- `{category}`: Kategori berita, misalnya `politik`

**Contoh:**
GET /news/category/kompas/politik

pgsql
Copy
Edit

## 🧪 Contoh Response JSON

```json
[
  {
    "title": "Judul Berita",
    "link": "https://example.com/berita",
    "date": "2025-08-01T10:30:00",
    "category": "politik",
    "portal": "kompas"
  }
]
🛠️ Teknologi yang Digunakan
Python 3.11+

FastAPI

SQLite

Uvicorn
