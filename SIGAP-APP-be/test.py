import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

# URL target
url = "https://jogja.tribunnews.com/"

# Membuat session dengan header yang lebih natural
session = requests.Session()

# Generate random user agent
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

try:
    # Mengirim permintaan HTTP GET dengan headers
    response = session.get(url, headers=headers, timeout=10)
    
    # Tambahkan delay untuk simulasi perilaku manusia
    time.sleep(2)
    
    # Memeriksa apakah permintaan berhasil
    if response.status_code == 200:
        # Parsing konten HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Contoh: Mengambil judul berita utama
        headlines = soup.find_all('h3', class_='f16')
        
        if not headlines:
            # Jika tidak ditemukan dengan class 'f16', coba alternatif selector
            headlines = soup.select('h3[class*="f16"], h3[class*="title"], h2[class*="title"]')
        
        print("Judul Berita Utama:")
        for idx, headline in enumerate(headlines[:10], start=1):  # Batasi 10 hasil
            title = headline.get_text(strip=True)
            if title:  # Hanya tampilkan jika ada teks
                print(f"{idx}. {title}")
                
    else:
        print(f"Gagal mengakses halaman. Status code: {response.status_code}")
        print("Response headers:", response.headers)

except requests.exceptions.RequestException as e:
    print(f"Error saat melakukan request: {e}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")