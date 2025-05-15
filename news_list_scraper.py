import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

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

        description_tag = item.find('div', class_='grey2 pt5 f13 ln18 txt-oev-2')
        description = description_tag.text.strip() if description_tag else None

        source_tag = item.find('a', class_='fbo2 tsa-2')
        source = source_tag.text.strip() if source_tag else None
        source_url = source_tag['href'] if source_tag else None

        time_tag = item.find('time', class_='foot timeago')
        time_published = time_tag.text.strip() if time_tag else None

        img_tag = item.select_one('div.fr.mt5.pos_rel img')
        img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        news_data.append({
            "title": title,
            "url": article_url,
            "description": description,
            "source": source,
            "source_url": source_url,
            "time_published": time_published,
            "image_url": img_url,
            "content": None
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

        source = "Tribun Jogja"
        source_url = "https://jogja.tribunnews.com/"
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
        category_tag = item.select_one('header')
        category = category_tag.text.strip() if category_tag else None
        datetime_tag = item.select_one('span.text-muted')
        datetime_text = None
        if datetime_tag:
            raw_text = datetime_tag.text.strip()
            # Jika formatnya seperti "4 jam yang lalu", gunakan tanggal hari ini
            if "yang lalu" in raw_text:
                now = datetime.now()
                datetime_text = now.strftime("%d %m %y")
            else:
                try:
                    dt = datetime.strptime(raw_text, "%d/%m/%Y %H:%M")
                    datetime_text = dt.strftime("%d %m %y")
                except Exception:
                    datetime_text = raw_text

        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'datetime': datetime_text,
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

        category_tag = item.select_one('span.text-warning')
        category = category_tag.text.strip() if category_tag else None

        date_tag = item.select_one('span.float-left.fn80')
        date = date_tag.text.strip() if date_tag else None

        viewers_tag = item.select_one('span.float-right.fn80')
        viewers = viewers_tag.text.strip() if viewers_tag else None

        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'date': date,
            'viewers': viewers,
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

        # Mengambil kategori
        category_tag = item.select_one('.latest__subtitle a')
        category = category_tag.text.strip() if category_tag else None

        # Mengambil tanggal dan waktu
        datetime_tag = item.select_one('.latest__date')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        # Menyusun hasil scraping dalam dictionary
        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'datetime': datetime_text,
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

        # Mengambil gambar
        image_tag = item.select_one('.most__img img')
        image_url = image_tag['src'] if image_tag else None

        # Mengambil nomor urut (ranking)
        number_tag = item.select_one('.most__number')
        number = number_tag.text.strip() if number_tag else None

        # Mengambil kategori (jika ada)
        category_tag = item.select_one('.most__right .latest__subtitle')
        category = category_tag.text.strip() if category_tag else None

        # Mengambil tanggal (jika ada)
        datetime_tag = item.select_one('.latest__date')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        # Menyusun hasil scraping dalam dictionary
        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'datetime': datetime_text,
            'number': number
        }
        
        # Menambahkan berita ke dalam list
        news_list.append(news)

    return news_list

def scrape_idntimes():
    url = 'https://jogja.idntimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('div#latest-article div.box-latest')

    for item in news_items:
        # Judul
        title_tag = item.select_one('h2.title-text')
        title = title_tag.text.strip() if title_tag else None

        # Link
        link_tag = item.select_one('a.box-panel')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        full_link = 'https://jogja.idntimes.com' + link if link and link.startswith('/') else link

        # Gambar
        image_tag = item.select_one('img')
        image_url = image_tag['src'] if image_tag else None

        # Kategori
        category_tag = item.select_one('span.category a')
        category = category_tag.text.strip() if category_tag else None

        # Waktu
        datetime_tag = item.select_one('time.date')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'datetime': datetime_text,
        }

        news_list.append(news)

    return news_list

def scrape_popular_idntimes():
    url = 'https://jogja.idntimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('div.box-trending')

    for item in news_items:
        # Judul
        title_tag = item.select_one('h2.title-text')
        title = title_tag.text.strip() if title_tag else None

        # Link
        link_tag = item.select_one('a.trending-click')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        full_link = 'https://jogja.idntimes.com' + link if link and link.startswith('/') else link

        # Gambar
        image_url = link_tag['data-image-url'] if link_tag and link_tag.has_attr('data-image-url') else None

        # Kategori
        category_tag = item.select_one('span.category a')
        category = category_tag.text.strip() if category_tag else None

        # Waktu
        datetime_tag = item.select_one('time.date')
        datetime_text = datetime_tag.text.strip() if datetime_tag else None

        news = {
            'title': title,
            'url': full_link,
            'image': image_url,
            'category': category,
            'datetime': datetime_text,
        }

        news_list.append(news)

    return news_list