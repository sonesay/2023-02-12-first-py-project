from helpers.api_request import APIRequest
from helpers.arc_sync import ArcSync
from helpers.web_scrapper import WebScraper

if __name__ == '__main__':
    scraper = WebScraper()
    arc_sync = ArcSync()

    test_urls = [
        # 'https://www.teaomaori.news/east-coast-jobs-could-flower-kanuka-oil',
        # 'https://www.teaomaori.news/new-plymouth-mayor-iwi-determined-see-toxic-dioxon-contaminated-whenua-fixed',
        # 'https://www.teaomaori.news/wahine-maori-and-husband-join-relief-efforts-following-turkey-earthquake-turkey',
        # 'https://www.teaomaori.news/rnz-tvnz-merger-scrapped',
        # 'https://www.teaomaori.news/28th-maori-battalion-memorial-flag-finally-flies-battle-honours',
        # 'https://www.teaomaori.news/one-missing-boats-torn-moorings-on-aotea-great-barrier-island',
        # 'https://www.teaomaori.news/police-dog-v-rangatahi-justified-ipca-says',
        # 'https://www.teaomaori.news/worried-auckland-coaches-and-players-national-maori-basketball-tournament',
        'https://www.teaomaori.news/green-party-announces-daughter-north-te-tai-tokerau-candidate'
    ]

    # Step 0
    arc_sync.delete_migration_test_images()
    arc_sync.delete_migration_test_stories()
    # arc_sync.test_get_site_sections()

    # Step 1
    # scraper.process_english_categories()

    # Step 2
    # scraper.scrape_full_article_page(test_urls)

    # Step 3
    arc_sync.sync_stories_to_arc(test_urls)

    # arc_sync.sync_authors_to_arc()
