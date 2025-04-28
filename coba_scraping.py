from bs4 import BeautifulSoup
import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

# Fungsi untuk scraping dashboard news
def scrape_dashboard_news():
    print("Scraping dashboard...")
    try:
        response = requests.get('https://jogja.tribunnews.com/', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dashboard: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find_all('li', class_='p1520 art-list pos_rel')

    news_data = []
    for item in news:
        title_tag = item.find('h3').find('a')
        title = title_tag.text.strip() if title_tag else None
        article_url = title_tag['href'] if title_tag else None

        description_tag = item.find('div', class_='grey2 pt5 f13 ln18 txt-oev-2')
        description = description_tag.text.strip() if description_tag else None

        source_tag = item.find('a', class_='fbo2 tsa-2')
        source = source_tag.text.strip() if source_tag else None
        source_url = source_tag['href'] if source_tag else None

        time_tag = item.find('time', class_='foot timeago')
        time_published = time_tag.text.strip() if time_tag else None

        image_tag = item.find('img')
        image_url = image_tag['src'] if image_tag else None

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
    news_data = scrape_dashboard_news()
    if not news_data:
        print("Tidak ada berita ditemukan.")
        return

    news_data_with_analysis = scrape_and_analyze_news(news_data)

    output_dir = 'database'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'tribun.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(news_data_with_analysis, json_file, ensure_ascii=False, indent=4)
        print(f"Data telah disimpan di {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

    print(f"Total waktu eksekusi: {time.time() - start_time:.2f} detik")

if __name__ == "__main__":
    main()
