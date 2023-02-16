from helpers.arc_sync import ArcSync
from helpers.web_scrapper import WebScraper

if __name__ == '__main__':
    scraper = WebScraper()
    arc_sync = ArcSync()

    # scraper.process_english_categories()
    # scraper.scrape_full_article_page()
    arc_sync.sync_to_arc()
