import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from slugify import slugify  # pip install python-slugify

# URL de base du site
BASE_URL = "http://books.toscrape.com/"

# Définir le dossier courant (où est le script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Définir un sous-dossier pour stocker les CSV
CSV_DIR = os.path.join(BASE_DIR, "csv")
os.makedirs(CSV_DIR, exist_ok=True)  # Crée le dossier s'il n'existe pas

# Fonction pour récupérer et parser une page web
def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Lève une erreur si la requête échoue
    return BeautifulSoup(response.text, "html.parser")

# Récupérer toutes les catégories disponibles sur la page d’accueil
def get_categories():
    soup = get_soup(BASE_URL)
    category_links = soup.select(".side_categories ul li ul li a")
    return {link.text.strip(): urljoin(BASE_URL, link["href"]) for link in category_links}

# Récupérer toutes les URL de livres pour une catégorie (avec gestion des pages)
def get_all_book_urls_from_category(category_url):
    book_urls = []
    while category_url:
        soup = get_soup(category_url)
        for a in soup.select("h3 a"):
            book_urls.append(urljoin(category_url, a["href"]))
        next_button = soup.select_one("li.next a")
        category_url = urljoin(category_url, next_button["href"]) if next_button else None
    return book_urls

# Extraire les données principales d’un livre à partir de son URL
def get_book_details(book_url):
    soup = get_soup(book_url)

    title = soup.h1.text.strip()
    upc = soup.find("th", string="UPC").find_next("td").text.strip()
    price_incl = soup.find("th", string="Price (incl. tax)").find_next("td").text.strip()
    price_excl = soup.find("th", string="Price (excl. tax)").find_next("td").text.strip()
    availability = soup.find("th", string="Availability").find_next("td").text.strip()
    description_tag = soup.select_one("#product_description ~ p")
    description = description_tag.text.strip() if description_tag else ""
    category = soup.select(".breadcrumb li")[2].text.strip()
    review = soup.select_one(".star-rating")["class"][1]

    return {
        "product_page_url": book_url,
        "universal_product_code": upc,
        "title": title,
        "price_including_tax": price_incl,
        "price_excluding_tax": price_excl,
        "number_available": availability,
        "product_description": description,
        "category": category,
        "review_rating": review,
    }

# Enregistrer les livres dans un fichier CSV par catégorie
def save_books_to_csv(books, category_name):
    if not books:
        return
    filename = os.path.join(CSV_DIR, f"{slugify(category_name)}.csv")
    fieldnames = books[0].keys()
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)

# Fonction principale pour scraper toutes les catégories et stocker les CSV
def scrape_all_categories():
    categories = get_categories()
    for category_name, category_url in categories.items():
        print(f"🔍 Catégorie : {category_name}")
        book_urls = get_all_book_urls_from_category(category_url)
        books_data = []
        for book_url in book_urls:
            try:
                book = get_book_details(book_url)
                books_data.append(book)
            except Exception as e:
                print(f"❌ Erreur avec le livre {book_url} : {e}")
        save_books_to_csv(books_data, category_name)
        print(f"✅ {len(books_data)} livres enregistrés dans {category_name}.csv\n")

# Exécution du script si lancé directement
if __name__ == "__main__":
    scrape_all_categories()
