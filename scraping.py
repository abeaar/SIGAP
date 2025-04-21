from bs4 import BeautifulSoup
import requests
import json

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
                "image_url": image_url
        })

# Export hasil scraping ke file JSON
with open('tribun.json', 'w', encoding='utf-8') as json_file:
        json.dump(news_data, json_file, ensure_ascii=False, indent=4)

print("Data has been exported to tribun.json")
