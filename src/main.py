# feline_finder/main.py

import src

# Initialize the cat repository using Parquet format
database = src.infrastructure.cat_repository.PolarsCatRepository(
    "/workspaces/feline-finder/database/cats.parquet"
)

# List existing cats in the repository
existing_cats = database.list_cats()
print("Existing cats in database:")
for cat in existing_cats:
    print(cat)

# Initialize the scraper for Safe Haven for Cats
scraper = src.infrastructure.scrapers.SafeHavenScraper()

# Scrape available cats
cats = scraper.get_available_cats()

# Add scraped cats to the repository and print them
for cat in cats:
    database.add_cat(cat)
    print(cat)
