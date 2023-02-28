import os

from helpers.arc_sync import ArcSync
from helpers.web_scrapper import WebScraper

if __name__ == '__main__':
    scraper = WebScraper()
    arc_sync = ArcSync()

    # Step 0
    arc_sync.delete_migration_test_images()

    # Step 1
    # scraper.process_english_categories()

    # Step 2
    # scraper.scrape_full_article_page()

    # Step 3
    arc_sync.sync_stories_to_arc()
