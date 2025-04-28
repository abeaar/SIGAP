from bs4 import BeautifulSoup
import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
source_url = "https://yogyakarta.kompas.com/"

# Fungsi untuk scraping dashboard news
def scrape_dashboard_news():
    print("Scraping dashboard (Kompas Yogyakarta)...")
    try:
        response = requests.get('https://yogyakarta.kompas.com/', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dashboard: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.select('div.articleList div.articleItem')

    news_data = []
    for item in news:
        a_tag = item.select_one('a.article-link')
        article_url = a_tag['href'] if a_tag else None

        title_tag = item.select_one('h2.articleTitle')
        title = title_tag.text.strip() if title_tag else None

        description = None  # Tidak ada description di list, mungkin bisa ambil saat detail scrape

        source_tag = item.select_one('div.articlePost-subtitle')
        source = source_tag.text.strip() if source_tag else None

        source_url = "https://yogyakarta.kompas.com"

        time_tag = item.select_one('div.articlePost-date')
        time_published = time_tag.text.strip() if time_tag else None

        image_tag = item.select_one('img')
        image_url = image_tag['data-src'] if image_tag and image_tag.has_attr('data-src') else (image_tag['src'] if image_tag else None)

        news_data.append({
            "title": title,
            "url": article_url,
            "description": description,
            "source": source,
            "source_url": source_url,
            "time_published": time_published,
            "image_url": image_url,
            "content": None
        })

    return news_data

def scrape_popular_news_kompas():
    print("Scraping popular news (Kompas)...")
    try:
        response = requests.get(source_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching popular news: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.select('div.mostList.-mostlist.-mostArticle div.mostItem-img')

    news_data = []
    for item in news:
        parent = item.find_parent('a')  # cari parent a jika ada
        article_url = parent['href'] if parent and parent.has_attr('href') else None

        image_tag = item.select_one('img')
        image_url = image_tag['data-src'] if image_tag and image_tag.has_attr('data-src') else (image_tag['src'] if image_tag else None)

        title = image_tag['alt'].strip() if image_tag and image_tag.has_attr('alt') else None

        description = None  # Tidak tersedia pada list populer
        source = "Kompas"
        time_published = None  # Tidak ada tanggal di list populer

        news_data.append({
            "title": title,
            "url": article_url,
            "description": description,
            "source": source,
            "source_url": source_url,
            "time_published": time_published,
            "image_url": image_url,
            "content": None
        })

    return news_data


def scrape_and_analyze_news(news_data):
    for idx, item in enumerate(news_data, start=1):
        url = item['url']
        if not url:
            continue
        
        print(f"[{idx}/{len(news_data)}] Scraping detail: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html_text = response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL {url}: {e}")
            continue

        soup = BeautifulSoup(html_text, 'lxml')
        news_paragraphs = soup.find_all('p')
        content = " ".join(para.get_text().strip() for para in news_paragraphs if para.get_text().strip())

        if content:
            prompt = (
                f"Berikut ini adalah sebuah berita:\n\n{content}\n\n"
                "Pertama, ringkas berita ini dan berikan solusi untuk masalah yang diangkat.\n"
                "Kedua, tentukan kategori berita ini. Pilih hanya satu dari: hukum, kriminal, politik, ekonomi, teknologi, pendidikan, hiburan, agama. "
                "Jawab kategori di bagian bawah setelah ringkasan dan solusi, format: 'Kategori: [nama_kategori]'."
            )
            try:
                ollama_response = requests.post(OLLAMA_URL, json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                }, timeout=60)
                ollama_response.raise_for_status()
                result_text = ollama_response.json().get("response", "")

                if "Kategori:" in result_text:
                    summary_solution, category_line = result_text.rsplit("Kategori:", 1)
                    item['solution'] = summary_solution.strip()
                    item['category'] = category_line.strip()
                else:
                    item['solution'] = result_text.strip()
                    item['category'] = "Unknown"

                item['content'] = content

            except requests.exceptions.RequestException as e:
                print(f"Error connecting to Ollama API: {e}")
                continue

        time.sleep(1)

    return news_data

# Main function
def main():
    start_time = time.time()
    news_data = scrape_popular_news_kompas()
    if not news_data:
        print("Tidak ada berita ditemukan.")
        return

    news_data_with_analysis = scrape_and_analyze_news(news_data)

    output_dir = 'database'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'kompas.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(news_data_with_analysis, json_file, ensure_ascii=False, indent=4)
        print(f"Data telah disimpan di {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

    print(f"Total waktu eksekusi: {time.time() - start_time:.2f} detik")

if __name__ == "__main__":
    main()
