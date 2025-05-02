import requests
from bs4 import BeautifulSoup
import csv
import os

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

def get_book_details(book_url):
    soup = get_soup(book_url)

    title = soup.h1.text.strip()
    upc = soup.find('th', string='UPC').find_next('td').text.strip()
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text.strip()
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text.strip()
    number_available = soup.find('th', string='Availability').find_next('td').text.strip()
    description_tag = soup.find('div', id='product_description')
    product_description = description_tag.find_next('p').text.strip() if description_tag else ""
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'http://books.toscrape.com/' + soup.find('div', class_='item active').img['src'].replace('../', '')

    return {
        'product_page_url': book_url,
        'universal_product_code (upc)': upc,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': rating,
        'image_url': image_url
    }

def get_all_book_urls_from_category(category_url):
    book_urls = []
    while True:
        soup = get_soup(category_url)
        for h3 in soup.find_all('h3'):
            relative_url = h3.a['href'].replace('../../../', '')
            full_url = 'http://books.toscrape.com/catalogue/' + relative_url
            book_urls.append(full_url)

        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.a['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page
        else:
            break

    return book_urls

def save_book_details(book_urls):
    output_path = os.path.join(os.path.dirname(__file__), 'poetry_books_details.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'product_page_url', 'universal_product_code (upc)', 'title',
            'price_including_tax', 'price_excluding_tax', 'number_available',
            'product_description', 'category', 'review_rating', 'image_url'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url in book_urls:
            book_data = get_book_details(url)
            writer.writerow(book_data)

    print(f"Données enregistrées dans {output_path}")

# Point d'entrée
if __name__ == '__main__':
    category_url = 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html'
    book_urls = get_all_book_urls_from_category(category_url)
    save_book_details(book_urls)
