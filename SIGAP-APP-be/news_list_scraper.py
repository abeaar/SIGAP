import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import re

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_time(raw_time):
    """
    Parse Indonesian relative time strings like '2 jam yang lalu', '1 jam lalu', 
    absolute date strings like '15/05/2025 22:10', '15 Mei 2025, 22:10 WIB',
    'Kamis, 15 Mei 2025 19:47 WIB', or 'Kamis, 15 Mei 2025'.
    Returns a string in '%Y-%m-%d %H:%M:%S' format or None if parsing fails.
    """
    indonesian_months = {
        "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
        "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
        "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
    }

    if "yang lalu" in raw_time or raw_time.endswith("lalu"):
        match = re.match(r"(\d+)\s+(\w+)(?:\s+yang)?\s+lalu", raw_time)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            delta = None
            if unit.startswith("jam"):
                delta = datetime.now() - timedelta(hours=value)
            elif unit.startswith("menit"):
                delta = datetime.now() - timedelta(minutes=value)
            elif unit.startswith("detik"):
                delta = datetime.now() - timedelta(seconds=value)
            elif unit.startswith("hari"):
                delta = datetime.now() - timedelta(days=value)
            else:
                delta = datetime.now()
            return delta.strftime("%Y-%m-%d %H:%M:%S")
        else:
            try:
                return datetime.strptime(raw_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return None
    else:
        # Try dd/mm/yyyy hh:mm
        try:
            return datetime.strptime(raw_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
        # Try "15 Mei 2025, 22:10 WIB"
        try:
            match = re.match(r"(\d{1,2}) (\w+) (\d{4}), (\d{2}:\d{2})", raw_time)
            if match:
                day = int(match.group(1))
                month_str = match.group(2)
                month = indonesian_months.get(month_str)
                year = int(match.group(3))
                time_part = match.group(4)
                if month:
                    dt_str = f"{year}-{month}-{day:02d} {time_part}:00"
                    return dt_str
        except Exception:
            pass
        # Try "Kamis, 15 Mei  2025 19:47 WIB" (with or without day name, extra spaces)
        try:
            match = re.match(
                r"(?:\w+, )?(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{2}:\d{2})", raw_time)
            if match:
                day = int(match.group(1))
                month_str = match.group(2)
                month = indonesian_months.get(month_str)
                year = int(match.group(3))
                time_part = match.group(4)
                if month:
                    dt_str = f"{year}-{month}-{day:02d} {time_part}:00"
                    return dt_str
        except Exception:
            pass
        # Try "Kamis, 15 Mei 2025" (with or without day name, no time)
        try:
            match = re.match(
                r"(?:\w+, )?(\d{1,2})\s+(\w+)\s+(\d{4})", raw_time)
            if match:
                day = int(match.group(1))
                month_str = match.group(2)
                month = indonesian_months.get(month_str)
                year = int(match.group(3))
                if month:
                    dt_str = f"{year}-{month}-{day:02d} 00:00:00"
                    return dt_str
        except Exception:
            pass
        return None
        


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
        url = title_tag['href'] if title_tag else None

        time_tag = item.find('time', class_='foot timeago')
        if time_tag:
            raw_time = time_tag.text.strip()
            try:
                # Try to parse if it's already in a datetime format
                time_published = datetime.strptime(raw_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                # If parsing fails, just use the raw text
                time_published = now if not raw_time else raw_time
        else:
            time_published = None

        img_tag = item.select_one('div.fr.mt5.pos_rel img')
        image = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        news_data.append({
            "title": title,
            "url": url,
            "image": image,
            "time_published": time_published,
            "scrape_time": now,
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
    populer_section = soup.select_one('div.mb20.populer')
    articles = populer_section.select('ul li.pb15.art-list') if populer_section else []

    news_data = []
    for item in articles:
        link_tag = item.select_one('div.mt5.mr110 h3 a')
        title = link_tag.text.strip() if link_tag else None
        url = link_tag['href'] if link_tag and link_tag.has_attr('href') else None

        image_tag = item.select_one('div.fr.pos_rel a img')
        image = image_tag['src'] if image_tag and image_tag.has_attr('src') else None

        time_tag = item.select_one('div.grey.pt3 time')
        if time_tag and time_tag.has_attr('title'):
            raw_time = time_tag['title']
            time_published = parse_time(raw_time)
        else:
            time_published = None

        news_data.append({
            "title": title,
            "url": url,
            "image": image,
            "time_published": time_published,
            "scrape_time": now
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
        url = title_tag['href'] if title_tag else None

        time_tag = item.select_one('div.media__date span')
        if time_tag:
            raw_time = time_tag.text.strip()
            time_published = parse_time(raw_time)
        else:
            time_published = None

        image = None
        image_tag = item.select_one('span.ratiobox')
        if image_tag:
            style = image_tag.get('style', '')
            if 'background-image:' in style and 'url("' in style:
                try:
                    image = style.split('url("')[1].split('")')[0]
                    image = image.replace("&quot;", '"')
                except IndexError:
                    image = None

        news_data.append({
            "title": title,
            "url": url,
            "image": image,
            "time_published": time_published,
            "scrape_time": now,
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
        title_tag = item.select_one('h3.media__title a')
        title = title_tag.text.strip() if title_tag else None
        url = title_tag['href'] if title_tag and title_tag.has_attr('href') else None

        image_span = item.select_one('span.ratiobox')
        image_style = image_span['style'] if image_span and image_span.has_attr('style') else ''
        image = None
        if 'background-image' in image_style:
            start = image_style.find('url("') + len('url("')
            end = image_style.find('")')
            image = image_style[start:end]

        date_tag = item.select_one('div.media__date span')
        time_published = parse_time(date_tag['title'].strip()) if date_tag and date_tag.has_attr('title') else None

        news_data.append({
            "title": title,
            "url": url,
            "image": image,
            "time_published": time_published,
            "scrape_time": now,
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
        url = 'https://jogja.times.co.id' + link if link.startswith('/') else link
        image_tag = item.select_one('img.imaged')
        image = image_tag['src'] if image_tag else None
        datetime_tag = item.select_one('span.text-muted')
        time_published = None
        if datetime_tag:
            raw_text = datetime_tag.text.strip()
            time_published = parse_time(raw_text)

        news = {
            'title': title,
            'url': url,
            'image': image,
            'time_published': time_published,
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
        url = 'https://jogja.times.co.id' + link if link and link.startswith('/') else link

        image_tag = item.select_one('img.card-img-top')
        image = image_tag['src'] if image_tag else None

        date_tag = item.select_one('span.float-left.fn80')
        time_published = parse_time(date_tag.text.strip()) if date_tag else None

        news = {
            'title': title,
            'url': url,
            'image': image,
            'time_published': time_published,
            'scrape_time': now,
        }
        news_list.append(news)

    return news_list

def scrape_kedaulatanrakyat():
    url = 'https://www.krjogja.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('.latest__item')

    for item in news_items:
        title_tag = item.select_one('.latest__title a')
        title = title_tag.text.strip() if title_tag else None

        link = title_tag['href'] if title_tag else None
        url = 'https://www.krjogja.com' + link if link and link.startswith('/') else link

        image_tag = item.select_one('div.latest__img a img')
        image = image_tag['src'] if image_tag else None

        datetime_tag = item.select_one('.latest__date')
        time_published = parse_time(datetime_tag.text.strip()) if datetime_tag else None

        news = {
            'title': title,
            'url': url,
            'image': image,
            'time_published': time_published,
            'scrape_time': now,
        }
        news_list.append(news)

    return news_list

def scrape_popular_kedaulatanrakyat():
    url = 'https://www.krjogja.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    news_items = soup.select('.most__item')

    for item in news_items:
        title_tag = item.select_one('.most__title')
        title = title_tag.text.strip() if title_tag else None

        link_tag = item.select_one('.most__link')
        link = link_tag['href'] if link_tag else None
        url = 'https://www.krjogja.com' + link if link and link.startswith('/') else link

        detail_response = requests.get(url, timeout=10)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, 'lxml')

        detail_image_tag = detail_soup.select_one('.photo__img img')
        image = detail_image_tag['src'] if detail_image_tag and detail_image_tag.has_attr('src') else None

        detail_date_tag = detail_soup.select_one('.read__info__date')
        time_published = parse_time(detail_date_tag.text.strip()) if detail_date_tag else None

        news = {
            'title': title,
            'url': url,
            'image': image,
            'time_published': time_published,
            'scrape_time': now,
        }
        news_list.append(news)

    return news_list

def scrape_idntimes():
    url = 'https://jogja.idntimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    news_list = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ambil semua elemen berita dari dalam container utama
    news_items = soup.select('div.css-hi7h29 div.css-v44eiu')

    for item in news_items:
        # Judul
        title_tag = item.select_one('h3[data-testid="title-article"]')
        title = title_tag.text.strip() if title_tag else None

        # URL
        link_tag = item.select_one('a[href]')
        link = link_tag['href'] if link_tag else None
        full_url = 'https://jogja.idntimes.com' + link if link and link.startswith('/') else link

        # Gambar
        image_tag = item.select_one('img')
        image = image_tag['src'] if image_tag else None

        # Kategori/Lokasi
        category_tag = item.select_one('span.css-544mn6')
        category = category_tag.text.strip() if category_tag else None

        # Tanggal/Waktu publikasi
        time_tag = item.select_one('span[data-testid="publish-date-article"]')
        time_published = time_tag.text.strip() if time_tag else None

        news = {
            'title': title,
            'url': full_url,
            'image': image,
            'category': category,
            'time_published': time_published,
            'scrape_time': now,
        }

        news_list.append(news)

    return news_list

def scrape_popular_idntimes():
    url = 'https://jogja.idntimes.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    news_list = []

    # Ambil kontainer utama berdasarkan struktur yang kamu berikan
    container = soup.select_one('div.css-mkj7m6 > div.css-a6dqqb > div.css-xw0iqe > div.css-1i344v0')

    if not container:
        print("⚠️ Kontainer berita tidak ditemukan.")
        return []

    news_items = container.select('div.css-1i55tqt')

    for item in news_items:
        # Judul berita
        title_tag = item.select_one('h3[data-testid="title-article"]')
        title = title_tag.text.strip() if title_tag else None

        # Link berita
        link_tag = item.select_one('a[href]')
        link = link_tag['href'] if link_tag else None
        full_url = 'https://jogja.idntimes.com' + link if link and link.startswith('/') else link

        # Gambar
        img_tag = item.select_one('img')
        image = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

        # Kategori
        category_tag = item.select_one('span.css-544mn6')
        category = category_tag.text.strip() if category_tag else None

        # Waktu publish
        time_tag = item.select_one('span[data-testid="publish-date-article"]')
        time_published = time_tag.text.strip() if time_tag else None

        news = {
            'title': title,
            'url': full_url,
            'image': image,
            'category': category,
            'time_published': time_published,
            'scrape_time': now,
        }

        news_list.append(news)

    return news_list