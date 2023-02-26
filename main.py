import os

from helpers.arc_id_generator import generate_arc_id
from helpers.arc_sync import ArcSync
from helpers.web_scrapper import WebScraper

if __name__ == '__main__':
    scraper = WebScraper()
    arc_sync = ArcSync()

    # url = "sites/default/files/styles/video_player_placeholder_image/public/news_article" \
    #       "/Napier_Angus_Dreaver.jpeg"
    # arc_id = generate_arc_id(os.environ.get('OWNER_ID'), url)

    # Step 1
    # scraper.process_english_categories()

    # Step 2
    # scraper.scrape_full_article_page()

    # Step 3
    arc_sync.sync_stories_to_arc()

    # Step 4
    # arc_sync.delete_migration_test_images()
