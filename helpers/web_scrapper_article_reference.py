from datetime import datetime
import requests
from bs4 import BeautifulSoup


class WebScraperArticleReference:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_news_article_references_from_url(self, category: str, url: str, page: int = 0,
                                             offset: int = 0) -> BeautifulSoup:
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

        print(f"Processed {category} category with data: {len(articles)} articles")

        # Check if there are more articles to process
        show_more_results_button = soup.select_one("#show-more-results-button a")
        if show_more_results_button is not None:
            offset = 20
            print(f"Found 'Show more news' button, going to next page {page + 1} with offset {offset}...")
            self.get_news_article_references_from_url(category, url, page + 1, offset)

        return soup
