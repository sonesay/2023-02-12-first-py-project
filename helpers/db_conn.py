import os
import sqlite3
from datetime import datetime

from dotenv import load_dotenv


class DbConn:
    def __init__(self):
        load_dotenv()  # load the .env file
        self.conn = sqlite3.connect(os.environ.get('DATABASE_FILE'))
        self.cursor = self.conn.cursor()

    def check_news_article_syncs(self, category):
        self.cursor.execute(
            f"SELECT page FROM news_article_syncs WHERE category = '{category}' ORDER BY page DESC LIMIT 1;")
        row = self.cursor.fetchone()
        if row is not None:
            return int(row[0])
        else:
            return None

    def set_article(self, category, title, published_date, author, page, request_url, link, featured_image_src):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # check if record already exists
        self.cursor.execute(
            f"SELECT id FROM news_article_syncs WHERE category = ? AND title = ?",
            (category, title)
        )
        row = self.cursor.fetchone()
        if row is not None:
            # update existing record
            self.cursor.execute(
                f"UPDATE news_article_syncs SET published_date = ?, author = ?, updated_at = ? WHERE id = ?",
                (published_date, author, now, row[0])
            )
            self.conn.commit()
        else:
            # insert new record
            if page is None:
                page = 0
            self.cursor.execute(
                f"INSERT INTO news_article_syncs (category, title, published_date, author, page, request_url, link, featured_image, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (category, title, published_date, author, page or 0, request_url, link, featured_image_src, now, now)
            )
            self.conn.commit()

    def get_tags_by_id(self, id):
        self.cursor.execute("SELECT tags FROM news_article_syncs WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if row is not None:
            tags_str = row[0]
            if tags_str is not None:
                tags_list = tags_str.split(", ")
                return tags_list
            else:
                return None
        else:
            return None

    def get_categories_by_link(self, link):
        self.cursor.execute("SELECT category FROM news_article_syncs WHERE link = ?", (link,))
        rows = self.cursor.fetchall()
        categories = []
        for row in rows:
            categories.append(row[0])
        return categories

    def update_author_id(self, record_id, author_id):
        self.cursor.execute(
            "UPDATE news_article_syncs SET author_id = ? WHERE id = ?",
            (author_id, record_id)
        )
        self.conn.commit()

    def get_distinct_authors(self):
        self.cursor.execute("SELECT DISTINCT author FROM news_article_syncs")
        rows = self.cursor.fetchall()
        authors = []
        for row in rows:
            authors.append(row[0])
        return authors

    def get_arc_id_by_link(self, link):
        self.cursor.execute("SELECT arc_id FROM news_article_syncs WHERE link = ? AND arc_id IS NOT NULL LIMIT 1",
                            (link,))
        row = self.cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
