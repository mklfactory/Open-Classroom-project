# 📚 Books to Scrape - Pipeline ETL

Ce projet automatise l'extraction, la transformation et le stockage des données du site [Books to Scrape](http://books.toscrape.com).

## 📦 Fonctionnalités

- 🔍 Extraction des livres depuis **toutes les catégories**
- 💾 Enregistrement des données produit dans des **fichiers CSV** par catégorie
- 🖼️ Téléchargement de l'image de couverture de chaque livre
- 📁 Stockage organisé dans un dossier `data/` contenant :
  - Un dossier `csv/` avec les données au format CSV
  - Un dossier `images/` contenant les couvertures de livres
- 📦 Création d’un **fichier ZIP (`data_export.zip`)** pour l’envoi des données

---

## ▶️ Instructions d'exécution

### 1. Cloner le repository

```bash
git clone <url_du_repository>
cd Books\ Online/Phase\ 6


### 2. Créer et activer un environnement virtuel

python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # macOS/Linux


### 3.installer les dépendances

pip install -r requirements.txt

### 4.Lancer le script
python product_scraper.py

