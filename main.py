from helpers.api_request import APIRequest
from helpers.arc_sync import ArcSync
from helpers.web_scrapper import WebScraper
from test_urls import test_urls

if __name__ == '__main__':
    scraper = WebScraper()
    arc_sync = ArcSync()

    # Step 0
    # arc_sync.sync_authors_to_arc()
    # arc_sync.test_get_site_sections()

    arc_sync.delete_migration_test_images()
    arc_sync.delete_migration_test_stories()

    # Step 1
    # scraper.process_english_categories()

    # Step 2
    # scraper.scrape_full_article_page(test_urls)

    # Step 3
    arc_sync.sync_stories_to_arc(test_urls)
