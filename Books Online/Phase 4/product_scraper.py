import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"

# Crée le dossier de sortie s'il n'existe pas
OUTPUT_DIR = "Books Online/Phase 4/csv"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_book_details(book_url):
    soup = get_soup(book_url)

    title = soup.find('h1').text.strip()

    # Table des infos
    table = soup.find('table', class_='table table-striped')
    rows = {row.th.text.strip(): row.td.text.strip() for row in table.find_all('tr')}
    upc = rows.get('UPC', '')
    price_including_tax = rows.get('Price (incl. tax)', '')
    price_excluding_tax = rows.get('Price (excl. tax)', '')
    availability = rows.get('Availability', '')
    number_available = ''.join(filter(str.isdigit, availability))

    # Catégorie
    category = soup.select('ul.breadcrumb li a')[-1].text.strip()

    # Description
    desc_tag = soup.select_one('article.product_page > p')
    description = desc_tag.text.strip() if desc_tag else ''

    # Note
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else 'None'

    # Image
    image_tag = soup.find('img')
    image_url = urljoin(book_url, image_tag['src']) if image_tag else ''

    return {
        'title': title,
        'upc': upc,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'category': category,
        'rating': rating,
        'description': description,
        'image_url': image_url,
        'product_page_url': book_url
    }

def extract_book_urls_from_category(category_url):
    book_urls = []
    while category_url:
        soup = get_soup(category_url)
        for h3 in soup.select('h3 a'):
            book_url = urljoin(category_url, h3['href'])  # 🛠️ Correction ici
            book_urls.append(book_url)
        next_button = soup.select_one('li.next > a')
        category_url = urljoin(category_url, next_button['href']) if next_button else None
    return book_urls

def save_books_to_csv(books_data, category_name):
    filename = f"{category_name.replace(' ', '_').lower()}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if books_data:
        keys = books_data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(books_data)
        print(f"✅ Fichier CSV créé : {filepath}")
    else:
        print(f"⚠️ Aucun livre trouvé pour la catégorie {category_name}")

def scrape_all_categories():
    homepage = get_soup(BASE_URL)
    category_links = homepage.select('div.side_categories ul li ul li a')

    for link in category_links:
        category_name = link.text.strip()
        category_url = urljoin(BASE_URL, link['href'])
        print(f"\n🔍 Catégorie : {category_name}")

        book_urls = extract_book_urls_from_category(category_url)
        books_data = [get_book_details(url) for url in book_urls]

        save_books_to_csv(books_data, category_name)

if __name__ == "__main__":
    scrape_all_categories()
