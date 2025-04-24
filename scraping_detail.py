from bs4 import BeautifulSoup
import requests
import json
import os

# Daftar URL yang akan di-scrape
# urls = [
#         'https://jogja.tribunnews.com/2025/04/24/progres-kasus-kekerasan-seksual-guru-besar-farmasi-ugm-pemeriksaan-internal-dimulai-mei',
#         'https://jogja.tribunnews.com/2025/04/24/ac-milan-kunci-juara-coppa-italia-menurut-tijjani-reijnders',
#         'https://jogja.tribunnews.com/2025/04/24/update-kabar-pemilik-raminten-meninggal-hamzah-sulaiman-disemayamkan-di-rumah-duka-pukj-yogyakarta'
# ]

with open("database/tribun.json", "r", encoding="utf-8") as file:
    data = json.load(file)

news_detail = []
urls = [item['url'] for item in data]

for url in urls:
        try:
                # Mendapatkan HTML dari URL
                response = requests.get(url)
                response.raise_for_status()  # Memastikan permintaan berhasil
                html_text = response.text
        except requests.exceptions.RequestException as e:
                print(f"Error fetching the URL {url}: {e}")
                continue

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_text, 'lxml')

        # Mengambil semua elemen <p>
        news = soup.find_all('p')

        # Menggabungkan semua teks dari elemen <p> menjadi satu string
        content = " ".join(para.get_text().strip() for para in news if para.get_text().strip())
        news_detail.append({"url": url, "content": content})

# Pastikan direktori untuk menyimpan file JSON ada
output_dir = 'database'
os.makedirs(output_dir, exist_ok=True)

# Export hasil scraping ke file JSON
output_file = os.path.join(output_dir, 'tribun_detail.json')
try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
                json.dump(news_detail, json_file, ensure_ascii=False, indent=4)
        print(f"Data has been exported to {output_file}")
except IOError as e:
        print(f"Error writing to file: {e}")
