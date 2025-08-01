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
  "portal": "detik",
    "category": "politik",
    "data": [
        {
            "id": 864,
            "title": "Jokowi Curiga Ada Agenda Jatuhkan Reputasinya di Balik Isu Ijazah Palsu",
            "url": "https://www.detik.com/jogja/berita/d-8011542/jokowi-curiga-ada-agenda-jatuhkan-reputasinya-di-balik-isu-ijazah-palsu",
            "image": null,
            "time_published": "2025-07-14 21:56:00",
            "scrape_time": "2025-07-15 08:56:00",
            "content": "Presiden ke-7 RI Joko Widodo (Jokowi) menilai ada agenda politik di balik isu soal ijazah palsu hingga pemakzulan Wakil Presiden Gibran Rakabuming Raka. Agenda itu ialah menurunkan reputasi politik dirinya. Dilansir detikJateng, polemik ijazah palsu Jokowi kembali muncul usai Jokowi purnatugas pada Oktober 2024 lalu. Jokowi bahkan melaporkan lima orang terkait isu ijazah palsu tersebut. \"Saya berperasaan, memang kelihatannya ada agenda besar politik. Dibalik isu-isu ini ijazah palsu, isu pemakzulan,\" kata Jokowi saat ditemui wartawan di kediaman pribadinya di Sumber, Banjarsari, Solo, Senin (14/6/2025). SCROLL TO CONTINUE WITH CONTENT Jokowi curiga agenda besar politik itu ingin menurunkan reputasi dirinya. Menurutnya, hal itu termasuk terkait isu pemakzulan Gibran. \"Ini perasaan politik saya mengatakan ada agenda besar politik untuk menurunkan reputasi politik, untuk men-down grade,\" ujar dia. \"Termasuk itu (isu pemakzulan) Jadi ijazah palsu, pemakzulan Mas Wapres, saya kira ada agenda besar politik,\" ucap Jokowi. Meski demikian, Jokowi menyatakan dirinya merespons itu secara biasa saja. \"Ya buat saya biasa-biasa aja lah dan biasa, ya bisa,\" pungkasnya.",
            "solution": "Ringkasan berita ini adalah sebagai berikut:\n\nPresiden ke-7 RI Joko Widodo (Jokowi) menyatakan bahwa ada agenda politik besar yang ingin menurunkan reputasinya, termasuk terkait isu pemakzulan Wakil Presiden Gibran Rakabuming Raka. Ia melaporkan lima orang terkait isu ijazah palsu dan berperasaan bahwa ada agenda politik itu. Jokowi menyatakan dirinya merespons secara biasa saja.\n\nSolusi untuk masalah yang diangkat adalah dengan memastikan bahwa ada transparansi dan kejujuran dalam pemerintahan, sehingga tidak ada agendanya yang ingin menurunkan reputasi seseorang. Selain itu, penting juga untuk meningkatkan kesadaran masyarakat tentang pentingnya integritas dan kejujuran dalam pemerintahan.",
            "category": "politik"
        },
        {
            "id": 841,
            "title": "Mutasi Polri, Kapolresta Jogja hingga Dirkrimsus Polda DIY Diganti",
            "url": "https://www.detik.com/jogja/berita/d-7981894/mutasi-polri-kapolresta-jogja-hingga-dirkrimsus-polda-diy-diganti",
            "image": null,
            "time_published": "2025-06-25 17:00:01",
            "scrape_time": "2025-06-26 03:00:01",
            "content": "Kapolri Jenderal Listyo Sigit Prabowo melakukan rotasi atau mutasi jabatan kapolres dan pejabat utama Polda DIY. Rotasi jabatan itu meliputi posisi Kapolresta Kota Jogja, Dir Reskrimsus Polda DIY, dan Itwasum Polda DIY. Adapun rotasi jabatan itu berdasarkan Surat Keputusan Kapolri Kep 927/VI/2025 tanggal 24 Juni 2025 dan STR Kapolri No 1422/VI/Kep/2025 tanggal 24 Juni 2025. \"Memang benar ada mutasi beberapa pejabat utama di Polda DIY,\" kata Kabid Humas Polda DIY Kombes Ihsan kepada wartawan di Mapolda DIY, Sleman, Rabu (26/6/2025). SCROLL TO CONTINUE WITH CONTENT Ihsan bilang pejabat yang dirotasi yakni Dirkrimsus Polda DIY Kombes Wirdhanto Hadicaksono. Dia digantikan oleh AKBP Saprodin yang sebelumnya menjabat Dirkrimsus Polda Sulbar. \"Pak Wirdhanto (dimutasi) jadi Dirkrimsus Polda Jabar,\" ujarnya. Kemudian, Kapolresta Jogja Kombes Aditya Surya Dharma dipromosikan sebagai Kasubdit Pam VIP Ditpamobvit Korps Sabhara Baharkam Polri. \"Adapun penggantinya adalah Kombes Eva Guna Pandia yang sebelumnya menjabat Karolog Polda Papua Barat,\" ucapnya. Kemudian pejabat Itwasda Polda DIY yang sebelumnya kosong, kini dijabat oleh Kombes I Gusti Ngurah Rai Mahaputra. Gusti sebelumnya Auditor Kepolisian Madya Tk. II Itwasum Polri. \"Sertijab nanti masih menunggu keputusan dari Bapak Kapolda,\" pungkasnya.",
            "solution": "Berikut adalah ringkasan berita:\n\nBerita ini membahas tentang rotasi jabatan beberapa pejabat utama di Polda DIY, termasuk Kapolresta Kota Jogja, Dir Reskrimsus Polda DIY, dan Itwasum Polda DIY. Rotasi jabatan ini dilakukan berdasarkan Surat Keputusan Kapolri dan STR Kapolri, dan melibatkan beberapa pejabat yang diangkat dan digantikan dalam posisi mereka.\n\nSolusi untuk masalah yang diangkat dalam berita ini adalah:\n\n* Sebagai solusi untuk rotasi jabatan yang dilakukan oleh Polda DIY, dapat dianut sebagai contoh bagi organisasi lain untuk melakukan rotasi jabatan secara teratur dan sesuai dengan kebutuhan.\n* Dapat juga disarankan agar pejabat yang diangkat memiliki pengalaman dan kemampuan yang lebih luas dalam menyelesaikan masalah dan meningkatkan kinerja organisasi.",
            "category": "politik"
        }
]
]
🛠️ Teknologi yang Digunakan
Python 3.11+

FastAPI

SQLite

Uvicorn
