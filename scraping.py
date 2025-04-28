from bs4 import BeautifulSoup
import requests
import json
import os

OLLAMA_URL = "http://localhost:11434/api/generate"

# Fungsi untuk scraping dashboard news
def scrape_dashboard_news():
    html_text = requests.get('https://jogja.tribunnews.com/').text
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('li', class_='p1520 art-list pos_rel')

    news_data = []
    for item in news:
        # Mengambil judul artikel
        title_tag = item.find('h3').find('a')
        title = title_tag.text.strip() if title_tag else None
        article_url = title_tag['href'] if title_tag else None

        # Mengambil deskripsi artikel
        description_tag = item.find('div', class_='grey2 pt5 f13 ln18 txt-oev-2')
        description = description_tag.text.strip() if description_tag else None

        # Mengambil sumber berita
        source_tag = item.find('a', class_='fbo2 tsa-2')
        source = source_tag.text.strip() if source_tag else None
        source_url = source_tag['href'] if source_tag else None

        # Mengambil waktu publikasi
        time_tag = item.find('time', class_='foot timeago')
        time_published = time_tag.text.strip() if time_tag else None

        # Mengambil gambar thumbnail
        image_tag = item.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Append hasil scraping ke list
        news_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "source": source,
                "source_url": source_url,
                "time_published": time_published,
                "image_url": image_url,
                "content": None  # Placeholder for content from the detail news
        })

    return news_data

# Fungsi untuk scraping detail berita dan analisis menggunakan Ollama API
def scrape_and_analyze_news(news_data):
    for item in news_data:
        url = item['url']
        if not url:
            continue
        
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

        # Kirimkan konten untuk analisis ringkasan dan solusi
        if content:
            # Ringkas dan berikan solusi
            solution_response = requests.post(OLLAMA_URL, json={
                "model": "llama3.2",
                "prompt": f"Ringkas Berikan solusi untuk berita berikut  :\n\n{content}",
                "stream": False
            })
            solution_data = solution_response.json()
            solution = solution_data.get("response", "")

            # Tentukan kategori berita
            category_response = requests.post(OLLAMA_URL, json={
                "model": "llama3.2",
                "prompt": f"Tentukan kategori berita ini. Pilih salah satu dari kategori berikut: hukum, kriminal, politik, ekonomi, teknologi, pendidikan, hiburan, agama. Hanya sebutkan kategori yang sesuai tanpa penjelasan. :\n\n{content}",
                "stream": False
            })
            category_data = category_response.json()
            category = category_data.get("response", "")

            # Menambahkan konten dan hasil analisis ke dalam data
            item['content'] = content
            item['solution'] = solution
            item['category'] = category

    return news_data

# Main function
def main():
    # Step 1: Scraping Dashboard News
    news_data = scrape_dashboard_news()

    # Step 2: Scraping detail news and analyze using Ollama
    news_data_with_analysis = scrape_and_analyze_news(news_data)

    # Step 3: Saving results to a single JSON file
    output_dir = 'database'
    os.makedirs(output_dir, exist_ok=True)

    # Save combined news data to a single file
    output_file = os.path.join(output_dir, 'tribun.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(news_data_with_analysis, json_file, ensure_ascii=False, indent=4)
        print(f"Combined data has been exported to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
