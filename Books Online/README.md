# 📚 Books to Scrape - ETL Pipeline

This project automates the **Extraction, Transformation, and Loading (ETL)** of book data from the [Books to Scrape](http://books.toscrape.com) website.

## 📦 Features

- 🔍 Extracts books from **all available categories**
- 💾 Saves book details into **CSV files**, one per category
- 🖼️ Downloads cover images for each book
- 📁 Organized storage in a `data/` folder containing:
  - A `csv/` folder with CSV files
  - An `images/` folder with cover images
- 📦 Creates a **ZIP archive (`data_export.zip`)** for easy sharing

---

## ▶️ How to Run the Script

### 1. Clone the Repository

```bash
git clone <repository_url>
cd "Books Online"
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Script

```bash
python product_scraper.py
```
