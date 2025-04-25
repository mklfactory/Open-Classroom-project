import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Exemple d'URL d'une page produit (modifiable)
PRODUCT_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def scrape_product(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur lors du chargement de la page produit.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # URL complète
    product_page_url = url

    # Table de spécifications produit
    table = soup.find("table", class_="table table-striped")
    rows = {row.th.text: row.td.text for row in table.find_all("tr")}

    upc = rows.get("UPC", "")
    price_including_tax = rows.get("Price (incl. tax)", "")
    price_excluding_tax = rows.get("Price (excl. tax)", "")
    number_available = rows.get("Availability", "").split(" ")[2].strip("()")

    title = soup.h1.text

    # Description
    description = soup.find("div", id="product_description")
    product_description = ""
    if description and description.find_next_sibling("p"):
        product_description = description.find_next_sibling("p").text.strip()

    # Catégorie
    category = soup.select_one("ul.breadcrumb li:nth-of-type(3) a").text

    # Note
    rating_class = soup.find("p", class_="star-rating")["class"][1]
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    review_rating = rating_map.get(rating_class, 0)

    # Image
    image_relative_url = soup.find("div", class_="item active").img["src"]
    image_url = urljoin(url, image_relative_url)

    # Écriture CSV
    with open("product_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "product_page_url", "universal_product_code", "title",
            "price_including_tax", "price_excluding_tax", "number_available",
            "product_description", "category", "review_rating", "image_url"
        ])
        writer.writerow([
            product_page_url, upc, title,
            price_including_tax, price_excluding_tax, number_available,
            product_description, category, review_rating, image_url
        ])

    print("Données produit extraites dans product_data.csv")

if __name__ == "__main__":
    scrape_product(PRODUCT_URL)
