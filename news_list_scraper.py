from bs4 import BeautifulSoup
import requests
from datetime import datetime

now = datetime.now().strftime("%d %m %Y")

def scrape_tribun():
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

        time_tag = item.find('time', class_='foot timeago')
        time_published = time_tag.text.strip() if time_tag else None

        image_tag = item.find('img')
        image_url = image_tag['src'] if image_tag else None

        news_data.append({
            "title": title,
            "url": article_url,
            "image": image_url,
            "time_published": time_published,
            "scrape_date": now
        })

    return news_data

def scrape_popular_tribun():
    print("Scraping Tribun Jogja Populer news...")
    try:
        response = requests.get('https://jogja.tribunnews.com/', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Tribun Jogja Populer news: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    
    # Hanya ambil artikel dari div dengan class "mb20 populer"
    populer_section = soup.select_one('div.mb20.populer')
    articles = populer_section.select('ul li.pb15.art-list') if populer_section else []

    news_data = []
    for item in articles:
        link_tag = item.select_one('div.mt5.mr110 h3 a')
        title = link_tag.text.strip() if link_tag else None
        article_url = link_tag['href'] if link_tag and link_tag.has_attr('href') else None

        image_tag = item.select_one('div.fr.pos_rel a img')
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

        time_tag = item.select_one('div.grey.pt3 time')
        time_published = time_tag['title'] if time_tag and time_tag.has_attr('title') else None

        news_data.append({
            "title": title,
            "url": article_url,
            "image": image_url,
            "time_published": time_published,
            "scrape_date": now
        })

    return news_data

def scrape_detik():
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


        time_tag = item.select_one('div.media__date span')
        time_published = time_tag.text.strip() if time_tag else None

        # Ambil gambar dari elemen span.ratiobox
        image_url = None
        image_tag = item.select_one('span.ratiobox')
        
        # Debug: Cek apakah image_tag ditemukan
        if image_tag:
            print("Image Tag Found!")
            # Debug: Menampilkan atribut style
            style = image_tag.get('style', '')
            print(f"Style Attribute: {style}")
            
            # Mengecek apakah ada background-image di style
            if 'background-image:' in style and 'url("' in style:
                try:
                    # Ekstrak URL gambar pertama
                    image_url = style.split('url("')[1].split('")')[0]
                    # Mengganti &quot; dengan tanda kutip ganda (")
                    image_url = image_url.replace("&quot;", '"')
                    print(f"Extracted Image URL: {image_url}")
                except IndexError:
                    print("Error extracting image URL")
                    image_url = None
            else:
                print("No valid background-image URL found in style")
        else:
            print("Image tag not found")

        news_data.append({
            "title": title,
            "url": article_url,
            "image": image_url,
            "time_published": time_published,
            "scrape_date": now,
        })

    return news_data

def scrape_popular_detik():
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
        # link_tag = item.select_one('a.media__title')
        # title = link_tag.text.strip() if link_tag else None
        # article_url = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        title_tag = item.select_one('h3.media__title a')
        title = title_tag.text.strip() if title_tag else None
        article_url = title_tag['href'] if title_tag and title_tag.has_attr('href') else None
        image_span = item.select_one('span.ratiobox')
        image_style = image_span['style'] if image_span and image_span.has_attr('style') else ''
        image_url = None
        if 'background-image' in image_style:
            start = image_style.find('url("') + len('url("')
            end = image_style.find('")')
            image_url = image_style[start:end]

        date_tag = item.select_one('div.media__date span')
        time_published = date_tag['title'].strip() if date_tag and date_tag.has_attr('title') else None

        news_data.append({
            "title": title,
            "url": article_url,
            "image": image_url,
            "time_published": time_published,
            "scrape_date": now,
        })

    return news_data

def scrape_times():
    url = 'https://jogja.times.co.id/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('#list_campaign li a.item')

    for item in news_items:
        title = item.select_one('h2').text.strip()
        link = item['href']
        full_link = 'https://jogja.times.co.id' + link if link.startswith('/') else link
        image_tag = item.select_one('img.imaged')
        image_url = image_tag['src'] if image_tag else None
        datetime_tag = item.select_one('span.text-muted')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'time_publish': datetime_text,
            'scrape_time': now,
        }
        news_list.append(news)

    return news_list

def scrape_popular_times():
    url = 'https://jogja.times.co.id/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('div.card.position-relative')

    for item in news_items:
        title_tag = item.select_one('h1')
        title = title_tag.text.strip() if title_tag else None

        link_tag = item.select_one('a.stretched-link')
        link = link_tag['href'] if link_tag else None
        full_link = 'https://jogja.times.co.id' + link if link and link.startswith('/') else link

        image_tag = item.select_one('img.card-img-top')
        image_url = image_tag['src'] if image_tag else None

        date_tag = item.select_one('span.float-left.fn80')
        date = date_tag.text.strip() if date_tag else None


        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'time_publish': date,
            'scrape_time': now,
        }
        news_list.append(news)

    return news_list

def scrape_kedaulatanrakyat():
    url = 'https://www.krjogja.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('.latest__item')  # Mengambil semua berita dari class 'latest__item'

    for item in news_items:
        # Mengambil judul
        title_tag = item.select_one('.latest__title a')
        title = title_tag.text.strip() if title_tag else None
        
        # Mengambil link berita
        link = title_tag['href'] if title_tag else None
        full_link = 'https://www.krjogja.com' + link if link and link.startswith('/') else link

        # Mengambil gambar
        image_tag = item.select_one('.latest__img img')
        image_url = image_tag['src'] if image_tag else None

        # Mengambil tanggal dan waktu
        datetime_tag = item.select_one('.latest__date')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        # Menyusun hasil scraping dalam dictionary
        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'time_publish': datetime_text,
            'scrape_time': now,
        }
        
        # Menambahkan berita ke dalam list
        news_list.append(news)

    return news_list


def scrape_popular_kedaulatanrakyat():
    url = 'https://www.krjogja.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('.most__item')  # Mengambil semua elemen berita di bagian populer

    for item in news_items:
        # Mengambil judul
        title_tag = item.select_one('.most__title')
        title = title_tag.text.strip() if title_tag else None

        # Mengambil link berita
        link_tag = item.select_one('.most__link')
        link = link_tag['href'] if link_tag else None
        full_link = 'https://www.krjogja.com' + link if link and link.startswith('/') else link
        # Scrap kembali dari sumber full_link untuk mengambil detail berita dan gambarnya
        detail_response = requests.get(full_link, timeout=10)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, 'lxml')

        # Mengambil gambar dari halaman detail jika tidak ada di halaman utama
        
        detail_image_tag = detail_soup.select_one('.photo__img img')
        image_url = detail_image_tag['src'] if detail_image_tag and detail_image_tag.has_attr('src') else None

        # Mengambil tanggal publikasi dari halaman detail jika tidak ada di halaman utama
      
        detail_date_tag = detail_soup.select_one('.read__info__date')
        datetime_text = detail_date_tag.text.strip() if detail_date_tag else None

        # Menyusun hasil scraping dalam dictionary
        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'time_publish': datetime_text,
            'scrape_time': now,
        }
        
        # Menambahkan berita ke dalam list
        news_list.append(news)

    return news_list
