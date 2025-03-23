# feline_finder/main.py

import src

scraper = src.infrastructure.scrapers.SafeHavenScraper()

cats = scraper.get_available_cats()

for cat in cats:
    print(f"{cat}")
