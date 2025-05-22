import json
import time
import requests
from bs4 import BeautifulSoup
import news_list_scraper

OLLAMA_URL = "http://localhost:11434/api/generate"

def scrape_and_analyze_news(news_data):
    for idx, item in enumerate(news_data, start=1):
        url = item.get('url')
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

                item['content'] = content
                
                if "Kategori:" in result_text:
                    summary_solution, category_line = result_text.rsplit("Kategori:", 1)
                    item['solution'] = summary_solution.strip()
                    item['category'] = category_line.strip()
                else:
                    item['solution'] = result_text.strip()
                    item['category'] = "Unknown"


            except requests.exceptions.RequestException as e:
                print(f"Error connecting to Ollama API: {e}")
                continue

        time.sleep(1)  # biar tidak terlalu cepat hit API

    return news_data

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
def main():
    portal_scrapers = {
        # 'tribun': news_list_scraper.scrape_tribun,
        # 'tribun_popular': news_list_scraper.scrape_popular_tribun,
        'detik': news_list_scraper.scrape_detik,
        'detik_popular': news_list_scraper.scrape_popular_detik,
        'times': news_list_scraper.scrape_times,
        'times_popular': news_list_scraper.scrape_popular_times,
        'kedaulatanrakyat': news_list_scraper.scrape_kedaulatanrakyat,
        'kedaulatanrakyat_popular': news_list_scraper.scrape_popular_kedaulatanrakyat,
        'idntimes': news_list_scraper.scrape_idntimes,
        'idntimes_popular': news_list_scraper.scrape_popular_idntimes,
    }

    total_start_time = time.time()  # Timer untuk keseluruhan proses

    for portal_name, scraper_func in portal_scrapers.items():  
        print(f"\n=== Scraping portal: {portal_name.upper()} ===")
        
        portal_start_time = time.time()  # Timer per portal

        news_list = scraper_func()
        print(f"Total news fetched: {len(news_list)}")

        news_list = scrape_and_analyze_news(news_list)

        save_path = f"database/{portal_name}.json"
        save_json(save_path, news_list)
        print(f"Saved {portal_name} news to {save_path}")

        portal_elapsed_time = time.time() - portal_start_time  # Hitung waktu per portal
        print(f"Finished scraping {portal_name.upper()} in {portal_elapsed_time:.2f} seconds.\n")

    total_elapsed_time = time.time() - total_start_time  # Hitung total waktu
    print(f"Total time for scraping all portals: {total_elapsed_time:.2f} seconds.\n")

if __name__ == "__main__":
    main()
