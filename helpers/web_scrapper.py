from helpers.db_conn import DbConn
from helpers.site_categories import SiteCategories
from helpers.web_scrapper_article_body import WebScraperArticleBody
from helpers.web_scrapper_article_reference import WebScraperArticleReference


class WebScraper:
    def __init__(self):
        self.db_conn = DbConn()
        self.article_body_scraper = WebScraperArticleBody(self.db_conn)
        self.article_reference_scraper = WebScraperArticleReference(self.db_conn)

    def process_english_categories(self):
        english_categories = SiteCategories.get_english_categories(self)
        for category, url in english_categories.items():
            highest_page = self.db_conn.check_news_article_syncs(category)
            if highest_page is not None:
                self.article_reference_scraper.get_news_article_references_from_url(category, url, highest_page, 20)
            else:
                self.article_reference_scraper.get_news_article_references_from_url(category, url)

    def scrape_full_article_page(self, test_urls=None):
        self.article_body_scraper.scrap_article_body_contents(test_urls)
