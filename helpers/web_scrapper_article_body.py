import requests
from bs4 import BeautifulSoup


class WebScraperArticleBody:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def scrap_article_body_contents(self):
        cursor = self.db_conn.conn.cursor()
        cursor.execute("SELECT * FROM news_article_syncs WHERE body IS NULL ORDER BY id ASC LIMIT 1;")
        rows = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]

        for row in rows:
            row_dict = {column_names[i]: value for i, value in enumerate(row)}
            url = row_dict['link']
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            # Extract the article body
            article_tag = soup.find("article")
            tags_div = article_tag.find("div", class_="field-news-tags")
            if tags_div:
                tags = [tag.text.strip() for tag in tags_div.find_all("a")]
                tags_str = ", ".join(tags)
                tags_div.extract()
                article_tag_str = str(article_tag)
                article_tag_str = article_tag_str.replace(str(tags_div), "")
                article_tag_str = article_tag_str.strip()
                cursor.execute("UPDATE news_article_syncs SET body=?, tags=? WHERE id=?",
                               (article_tag_str, tags_str, row_dict['id']))
            else:
                cursor.execute("UPDATE news_article_syncs SET body=? WHERE id=?", (str(article_tag), row_dict['id']))

            print(f"Processed article: {row_dict['published_date']} - {row_dict['title']} - by {row_dict['author']} ")

        self.db_conn.conn.commit()
        cursor.close()
