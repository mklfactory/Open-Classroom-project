# product_scraper.py

import os
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# Base URL of the website
BASE_URL = "http://books.toscrape.com/"
# Paths to save the extracted data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")
IMG_DIR = os.path.join(DATA_DIR, "images")

# Create directories if they do not exist
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)


def get_soup(url):
    """Returns the HTML content of a page as a BeautifulSoup object"""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return BeautifulSoup(response.content, "html.parser")


def sanitize_filename(text):
    """Sanitizes a string to make it a valid filename"""
    return re.sub(r'[\\/*?:"<>|]', "", text).strip().replace(" ", "_")


def get_categories():
    """Returns a dictionary {name: url} of all categories"""
    soup = get_soup(BASE_URL)
    categories = soup.select(".side_categories ul li ul li a")
    return {cat.get_text(strip=True): urljoin(BASE_URL, cat['href']) for cat in categories}


def get_book_urls_from_category(category_url):
    """Returns all the book URLs from a category (including pagination)"""
    urls = []
    while category_url:
        soup = get_soup(category_url)
        books = soup.select("h3 a")
        urls += [urljoin(category_url, book["href"]) for book in books]
        next_page = soup.select_one("li.next a")
        category_url = urljoin(category_url, next_page["href"]) if next_page else None
    return urls


def download_image(img_url, title, category):
    """Downloads a book's cover image and saves it locally"""
    response = requests.get(img_url)
    response.raise_for_status()  # Ensure the image is downloaded successfully
    category_dir = os.path.join(IMG_DIR, sanitize_filename(category))
    os.makedirs(category_dir, exist_ok=True)  # Create category folder if it doesn't exist
    img_filename = f"{sanitize_filename(title)}.jpg"  # Name the image file based on the book title
    path = os.path.join(category_dir, img_filename)  # Full path to save the image
    with open(path, "wb") as f:
        f.write(response.content)  # Write the image content to the file
    return path


def get_book_details(book_url, category):
    """Extracts all details of a book from its page"""
    soup = get_soup(book_url)
    title = soup.find("h1").text  # Get the book title
    table = soup.find("table")  # Extract book details from the table
    data = {row.find("th").text: row.find("td").text for row in table.find_all("tr")}
    description = soup.select_one("#product_description ~ p")  # Get the book description
    image_relative_url = soup.select_one("div.item.active img")["src"]  # Get the relative image URL
    image_url = urljoin(book_url, image_relative_url)  # Get the full image URL
    image_path = download_image(image_url, title, category)  # Download and save the image

    # Return all book details
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
    """Saves the books of a category to a CSV file"""
    if not books:  # If there are no books, do nothing
        return
    keys = books[0].keys()  # Get the keys (column headers)
    filename = os.path.join(CSV_DIR, f"{sanitize_filename(category)}.csv")  # Path to save the CSV file
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()  # Write the header (column names)
        writer.writerows(books)  # Write all book data


def scrape_all():
    """Runs the full pipeline: all categories, all books, saving CSV and images"""
    categories = get_categories()  # Get all categories
    for category, category_url in categories.items():
        print(f"🔍 Category: {category}")
        book_urls = get_book_urls_from_category(category_url)  # Get all book URLs in the category
        books = []
        for book_url in book_urls:
            try:
                books.append(get_book_details(book_url, category))  # Get book details and add to list
            except Exception as e:
                print(f"❌ Error on {book_url}: {e}")  # Print error if something goes wrong
        save_to_csv(books, category)  # Save the book data to CSV
    print("✅ Extraction complete!")


if __name__ == "__main__":
    scrape_all()  # Run the scraping process when the script is executed
