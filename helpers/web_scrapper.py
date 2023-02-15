from datetime import datetime
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
                self.scrape_html_from_url(category, url, highest_page, 20)
            else:
                self.scrape_html_from_url(category, url)

    def scrape_html_from_url(self, category: str, url: str, page: int = 0, offset: int = 0) -> BeautifulSoup:
        full_url = f"{url}&page={page}"
        if offset > 0:
            full_url += f"&offset={offset}"
        print(f"full_url: {full_url}")
        response = requests.get(full_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")
        print(f"Found {len(articles)} articles")
        for article in articles:
            # process the article tag here
            title = article.find("h3", class_="node-title").text.strip().replace("\n", "")
            # extract credits
            credits_div = article.find("div", class_="credits")
            author = credits_div.text.strip() if credits_div else ""
            if author.startswith('By '):
                author = author.replace('By ', '', 1)
            # extract datetime
            datetime_tag = article.find("time", class_="time-ago")
            published_date = datetime.strptime(datetime_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z').strftime(
                '%Y-%m-%d %H:%M:%S')
            # extract article link
            link = article.find("a", itemprop="mainEntityOfPage")['href']

            self.db_conn.set_article(category, title, published_date, author, page, full_url, link)

            print(f"Processed article: {published_date} - {title} - by {author} ")

        print(f"Processed {category} category with data: {soup}")
        return soup

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
