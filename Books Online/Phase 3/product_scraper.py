import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"

def get_book_details(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        title = soup.find('h1').text
    except: title = ''

    try:
        upc = soup.find('th', string='UPC').find_next('td').text
    except: upc = ''

    try:
        price_incl = soup.find('th', string='Price (incl. tax)').find_next('td').text
    except: price_incl = ''

    try:
        price_excl = soup.find('th', string='Price (excl. tax)').find_next('td').text
    except: price_excl = ''

    try:
        availability = soup.find('th', string='Availability').find_next('td').text.strip()
    except: availability = ''

    try:
        description = soup.find('meta', {'name': 'description'})
        description = description['content'].strip() if description else ''
    except: description = ''

    try:
        category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    except: category = ''

    try:
        review = soup.find('p', class_='star-rating')['class'][1]
    except: review = ''

    try:
        image_rel_url = soup.find('div', class_='item active').img['src']
        image_url = urljoin(BASE_URL, image_rel_url)
    except: image_url = ''

    return {
        'title': title,
        'upc': upc,
        'price_including_tax': price_incl,
        'price_excluding_tax': price_excl,
        'number_available': availability,
        'product_description': description,
        'category': category,
        'review_rating': review,
        'image_url': image_url,
        'product_page_url': book_url
    }

def get_book_urls(category_url):
    book_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for h3 in soup.find_all('h3'):
            partial_url = h3.find('a')['href']
            full_url = urljoin(category_url, partial_url)
            book_urls.append(full_url)

        next_li = soup.find('li', class_='next')
        if next_li:
            next_url = next_li.find('a')['href']
            category_url = urljoin(category_url, next_url)
        else:
            category_url = None

        time.sleep(1)  # pour être poli avec le serveur

    return book_urls

def save_books_to_csv(book_urls, output_file):
    if not book_urls:
        print("Aucune URL trouvée.")
        return

    books_data = []
    for url in book_urls:
        print(f"Scraping: {url}")
        data = get_book_details(url)
        books_data.append(data)
        time.sleep(1)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=books_data[0].keys())
        writer.writeheader()
        writer.writerows(books_data)

    print(f"{len(books_data)} livres enregistrés dans {output_file}")

# Exécution
category_url = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

output_csv = r"C:\Users\mklfa\Documents\GitHub\Open-Classroom-project\Books Online\Phase 3\poetry_books_details.csv"
book_urls = get_book_urls(category_url)
save_books_to_csv(book_urls, output_csv)
print(f"{len(book_urls)} livres trouvés")
