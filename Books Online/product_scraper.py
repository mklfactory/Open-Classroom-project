# product_scraper.py

import os
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

BASE_URL = "http://books.toscrape.com/"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")
IMG_DIR = os.path.join(DATA_DIR, "images")

# Crée les dossiers si non existants
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)


def get_soup(url):
    """Renvoie le contenu HTML d'une page en tant que soup"""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def sanitize_filename(text):
    """Nettoie un nom de fichier"""
    return re.sub(r'[\\/*?:"<>|]', "", text).strip().replace(" ", "_")


def get_categories():
    """Renvoie un dictionnaire {nom: url} de toutes les catégories"""
    soup = get_soup(BASE_URL)
    categories = soup.select(".side_categories ul li ul li a")
    return {cat.get_text(strip=True): urljoin(BASE_URL, cat['href']) for cat in categories}


def get_book_urls_from_category(category_url):
    """Renvoie toutes les URLs des livres d'une catégorie (pagination comprise)"""
    urls = []
    while category_url:
        soup = get_soup(category_url)
        books = soup.select("h3 a")
        urls += [urljoin(category_url, book["href"]) for book in books]
        next_page = soup.select_one("li.next a")
        category_url = urljoin(category_url, next_page["href"]) if next_page else None
    return urls


def download_image(img_url, title, category):
    """Télécharge l'image d'un livre et la sauvegarde"""
    response = requests.get(img_url)
    response.raise_for_status()
    category_dir = os.path.join(IMG_DIR, sanitize_filename(category))
    os.makedirs(category_dir, exist_ok=True)
    img_filename = f"{sanitize_filename(title)}.jpg"
    path = os.path.join(category_dir, img_filename)
    with open(path, "wb") as f:
        f.write(response.content)
    return path


def get_book_details(book_url, category):
    """Extrait toutes les infos d'un livre"""
    soup = get_soup(book_url)
    title = soup.find("h1").text
    table = soup.find("table")
    data = {row.find("th").text: row.find("td").text for row in table.find_all("tr")}
    description = soup.select_one("#product_description ~ p")
    image_relative_url = soup.select_one("div.item.active img")["src"]
    image_url = urljoin(book_url, image_relative_url)
    image_path = download_image(image_url, title, category)

    return {
        "title": title,
        "upc": data.get("UPC", ""),
        "price_including_tax": data.get("Price (incl. tax)", ""),
        "price_excluding_tax": data.get("Price (excl. tax)", ""),
        "number_available": data.get("Availability", ""),
        "description": description.text.strip() if description else "",
        "category": category,
        "review_rating": data.get("Number of reviews", ""),
        "image_url": image_url,
        "image_path": image_path,
        "product_page_url": book_url
    }


def save_to_csv(books, category):
    """Sauvegarde les livres d'une catégorie dans un CSV"""
    if not books:
        return
    keys = books[0].keys()
    filename = os.path.join(CSV_DIR, f"{sanitize_filename(category)}.csv")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)


def scrape_all():
    """Lance le pipeline complet : toutes les catégories, tous les livres, CSV et images"""
    categories = get_categories()
    for category, category_url in categories.items():
        print(f"🔍 Catégorie : {category}")
        book_urls = get_book_urls_from_category(category_url)
        books = []
        for book_url in book_urls:
            try:
                books.append(get_book_details(book_url, category))
            except Exception as e:
                print(f"❌ Erreur sur {book_url} : {e}")
        save_to_csv(books, category)
    print("✅ Extraction complète !")


if __name__ == "__main__":
    scrape_all()
