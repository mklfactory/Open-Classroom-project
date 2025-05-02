import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from slugify import slugify  # pip install python-slugify

BASE_URL = "http://books.toscrape.com/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_categories():
    soup = get_soup(BASE_URL)
    category_links = soup.select(".side_categories ul li ul li a")
    return {link.text.strip(): urljoin(BASE_URL, link["href"]) for link in category_links}

def get_all_book_urls_from_category(category_url):
    book_urls = []
    while category_url:
        soup = get_soup(category_url)
        for h3 in soup.select("h3 a"):
            book_urls.append(urljoin(category_url, h3["href"]))
        next_link = soup.select_one("li.next a")
        if next_link:
            category_url = urljoin(category_url, next_link["href"])
        else:
            break
    return book_urls

def download_image(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def get_book_details(book_url, category_name):
    soup = get_soup(book_url)

    title = soup.h1.text.strip()
    upc = soup.find("th", string="UPC").find_next("td").text.strip()
    price_incl = soup.find("th", string="Price (incl. tax)").find_next("td").text.strip()
    price_excl = soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()
    availability = soup.find("th", string="Availability").find_next("td").text.strip()
    description = soup.select_one("#product_description ~ p")
    description_text = description.text.strip() if description else ""
    category = soup.select_one(".breadcrumb li:nth-of-type(3) a").text.strip()
    review_rating = soup.select_one(".star-rating")["class"][1]
    image_relative_url = soup.select_one(".item.active img")["src"]
    image_url = urljoin(book_url, image_relative_url)

    # Image filename
    image_folder = os.path.join("images", slugify(category_name))
    image_filename = slugify(title) + os.path.splitext(urlparse(image_url).path)[-1]
    image_path = os.path.join(image_folder, image_filename)

    # Download image
    download_image(image_url, image_path)

    return {
        "product_page_url": book_url,
        "universal_product_code": upc,
        "title": title,
        "price_including_tax": price_incl,
        "price_excluding_tax": price_excl,
        "number_available": availability,
        "product_description": description_text,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
        "image_path": image_path
    }

def save_books_to_csv(books, category_name):
    if not books:
        return

    fieldnames = books[0].keys()
    os.makedirs("csv", exist_ok=True)
    filename = os.path.join("csv", f"{slugify(category_name)}.csv")
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

def scrape_all_categories():
    categories = get_categories()
    for name, url in categories.items():
        print(f"📚 Catégorie : {name}")
        book_urls = get_all_book_urls_from_category(url)
        books_data = []
        for book_url in book_urls:
            try:
                data = get_book_details(book_url, name)
                books_data.append(data)
            except Exception as e:
                print(f"❌ Erreur avec {book_url} : {e}")
        save_books_to_csv(books_data, name)
        print(f"✅ Fichier CSV généré pour la catégorie {name} ({len(books_data)} livres)\n")

if __name__ == "__main__":
    scrape_all_categories()
