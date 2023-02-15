import requests
from bs4 import BeautifulSoup
from helpers.db_conn import DbConn
from helpers.site_categories import SiteCategories


class WebScraper:
    def __init__(self):
        self.db_conn = DbConn()

    def process_english_categories(self):
        english_categories = SiteCategories.get_english_categories(self)
        for category, url in english_categories.items():
            highest_page = self.db_conn.check_news_article_syncs(category)
            if highest_page is not None:
                # Continue scraping from last page
                url += f'&page={highest_page}'
            else:
                # Start scraping from page 1
                url += '&page=1'

            html = self.fetch_page(url)
            parsed_data = self.parse_html(html)
            # process the parsed data for this category here
            print(f"Processed {category} category with data: {parsed_data}")

    def fetch_page(self, url):
        response = requests.get(url)
        return response.text

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # add your parsing logic here
        return soup

    def check_news_article_syncs(self, category):
        # Execute query to check news_article_syncs table for highest page number
        self.cursor.execute(
            f"SELECT * FROM news_article_syncs WHERE category = '{category}' ORDER BY page DESC LIMIT 1;")
        row = self.cursor.fetchone()
        if row is not None:
            # Return highest page number
            return row[1]
        else:
            # No rows found
            return None
