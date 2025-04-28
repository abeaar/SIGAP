from bs4 import BeautifulSoup
import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

# Fungsi untuk scraping dashboard news
def scrape_dashboard_news():
    print("Scraping dashboard (Detik Jogja)...")
    try:
        response = requests.get('https://www.detik.com/jogja', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dashboard: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.select('div.list-content.target_item article.list-content__item')

    news_data = []
    for item in news:
        title_tag = item.select_one('h3.media__title a')
        title = title_tag.text.strip() if title_tag else None
        article_url = title_tag['href'] if title_tag else None

        description = None  # Tidak ada di Detik list
        source = "Detik Jogja"
        source_url = "https://www.detik.com/jogja"

        time_tag = item.select_one('div.media__date span')
        time_published = time_tag.text.strip() if time_tag else None

        image_url = None
        image_tag = item.select_one('span.ratiobox')
        if image_tag and 'background-image' in image_tag.get('style', ''):
            style = image_tag['style']
            try:
                image_url = style.split('url("')[1].split('")')[0]
            except IndexError:
                image_url = None

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

def scrape_detikjogja_news():
    print("Scraping DetikJogja news...")
    try:
        response = requests.get('https://www.detik.com/terpopuler/jogja/', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching DetikJogja news: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    articles = soup.select('div.grid-row.list-content article.list-content__item')

    news_data = []
    for item in articles:
        link_tag = item.select_one('a.media__link')
        title = link_tag.text.strip() if link_tag else None
        article_url = link_tag['href'] if link_tag and link_tag.has_attr('href') else None

        image_span = item.select_one('span.ratiobox')
        image_style = image_span['style'] if image_span and image_span.has_attr('style') else ''
        image_url = None
        if 'background-image' in image_style:
            start = image_style.find('url("') + len('url("')
            end = image_style.find('")')
            image_url = image_style[start:end]

        date_tag = item.select_one('div.media__date span')
        time_published = date_tag['title'].strip() if date_tag and date_tag.has_attr('title') else None

        source = "detikJogja"
        source_url = "https://www.detik.com/terpopuler/jogja/"
        description = None  # Tidak ada deskripsi pendek di sini

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
    news_data = scrape_detikjogja_news()
    if not news_data:
        print("Tidak ada berita ditemukan.")
        return

    news_data_with_analysis = scrape_and_analyze_news(news_data)

    output_dir = 'database'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'detik.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(news_data_with_analysis, json_file, ensure_ascii=False, indent=4)
        print(f"Data telah disimpan di {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

    print(f"Total waktu eksekusi: {time.time() - start_time:.2f} detik")

if __name__ == "__main__":
    main()
