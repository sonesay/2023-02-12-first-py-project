import json
from collections import namedtuple
from html2ans.default import Html2Ans
from helpers.db_conn import DbConn
from helpers.site_categories import SiteCategories
from helpers.web_scrapper_article_reference import WebScraperArticleReference
from models.story import Headlines, Story


class WebScraper:
    def __init__(self):
        self.db_conn = DbConn()
        self.article_reference_scraper = WebScraperArticleReference(self.db_conn)

    def process_english_categories(self):
        english_categories = SiteCategories.get_english_categories(self)
        for category, url in english_categories.items():
            highest_page = self.db_conn.check_news_article_syncs(category)
            if highest_page is not None:
                self.article_reference_scraper.get_news_article_references_from_url(category, url, highest_page, 20)
            else:
                self.article_reference_scraper.get_news_article_references_from_url(category, url)

    def scrape_full_article_page(self):
        cursor = self.db_conn.conn.cursor()
        cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NOT NULL ORDER BY id ASC LIMIT 1;")
        rows = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]

        for row in rows:
            print(row)
            print(row['id'])
            parser = Html2Ans()
            content_elements = parser.generate_ans(row['body'])
            content_elements = [elem for elem in content_elements if elem['type'] != 'image']
            print(content_elements)
            content_elements_str = str(content_elements)

            # Create a namedtuple to represent the row for convenience
            # (Optional, but recommended)
            NewsArticle = namedtuple('NewsArticle', column_names)
            news_article = NewsArticle(*row)

            # Delete any existing arc stories with matching id
            response_delete = self.api_request.delete_arc_story(news_article)

            headlines = Headlines(news_article.title)
            story = Story("story", "0.10.9", "teaomaori", headlines)
            story.content_elements = content_elements;

            response_post = self.api_request.post_to_arc_migration_content(
                "https://api.sandbox.whakaatamaori.arcpublishing.com/draft/v1/story", story)

            # Extract the id from the response
            response_data = json.loads(response_post)
            arc_id = response_data['id']

            # Update the new_article_syncs table with the arc_id
            cursor.execute("UPDATE news_article_syncs SET arc_id=? WHERE id=?", (arc_id, row['id']))

        self.db_conn.conn.commit()
        cursor.close()
